"""
Pipeline principal de coleta de dados reais.
Orquestra todos os coletores e popula o banco SQLite.
"""
import json
import unicodedata
from database import get_db, init_db

from collectors.tse_collector import (
    buscar_candidatos_2026, buscar_bens_candidato, buscar_prestacao_contas,
    normalize_nome,
)
from collectors.datajud_collector import (
    buscar_processos_por_nome, mapear_processo_para_modelo,
)
from collectors.camara_collector import obter_historico_legislativo
from collectors.news_collector import buscar_materias_candidato, buscar_materias_candidato_fallback


def coletar_tudo():
    """
    Pipeline completo:
    1. Busca candidatos de 2026 no TSE
    2. Para cada candidato:
       - Busca bens declarados (TSE)
       - Busca prestação de contas (TSE)
       - Busca processos (DataJud)
       - Busca matérias (GNews/NewsAPI)
       - Busca histórico legislativo (Câmara/Senado)
    3. Salva tudo no banco
    """
    print("=" * 60)
    print("  CandidatAI — Pipeline de Coleta de Dados Reais")
    print("=" * 60)

    conn = get_db()
    cursor = conn.cursor()

    # Buscar candidatos de 2026
    print("\n[1/6] Buscando candidatos no TSE...")
    cargos = ["presidente", "governador", "senador", "deputado-federal"]
    todos_candidatos = []

    for cargo in cargos:
        candidatos = buscar_candidatos_2026(cargo=cargo)
        print(f"  {cargo}: {len(candidatos)} encontrados")
        todos_candidatos.extend(candidatos)

    if not todos_candidatos:
        print("  ⚠️ Nenhum candidato encontrado nas APIs. Usando dados mock como fallback.")
        from mock_data import seed_data
        seed_data()
        conn.close()
        return

    print(f"  Total: {len(todos_candidatos)} candidatos")

    # Para cada candidato, coletar dados complementares
    total = len(todos_candidatos)
    for idx, cand in enumerate(todos_candidatos):
        nome = cand.get("nome", cand.get("nomeUrna", ""))
        nome_norm = normalize_nome(nome)
        print(f"\n[{idx + 1}/{total}] Processando: {nome}")

        # Bens
        print("  → Buscando bens declarados...")
        bens = buscar_bens_candidato(cand.get("id", ""))
        print(f"    {len(bens)} bens encontrados")

        # Prestação de contas
        print("  → Buscando prestação de contas...")
        contas = buscar_prestacao_contas(cand.get("id", ""))
        print(f"    Total declarado: R$ {contas.get('total_declarado', 0):,.2f}")

        # Processos
        print("  → Buscando processos no DataJud...")
        processos_raw = buscar_processos_por_nome(nome)
        processos = [mapear_processo_para_modelo(p) for p in processos_raw]
        print(f"    {len(processos)} processos encontrados")

        # Histórico legislativo
        print("  → Buscando histórico legislativo...")
        historico = obter_historico_legislativo(nome)

        # Matérias
        print("  → Buscando matérias na mídia...")
        materias = buscar_materias_candidato(nome) or buscar_materias_candidato_fallback(nome) or []
        print(f"    {len(materias)} matérias encontradas")

        # Salvar no banco
        try:
            cursor.execute(
                """INSERT INTO candidatos (nome, nome_normalizado, numero, partido, cargo, estado, foto_url,
                   intencao_voto, pesquisa_fonte, indicadores)
                   VALUES (?, ?, ?, ?, ?, ?, ?, NULL, NULL, ?)""",
                (
                    nome, nome_norm,
                    cand.get("numero", None),
                    cand.get("partido", cand.get("siglaPartido", "Indefinido")),
                    cand.get("cargo", cand.get("descricaoCargo", cargo)),
                    cand.get("estado", cand.get("uf", "Nacional")),
                    cand.get("fotoUrl", ""),
                    json.dumps({
                        "processos_totais": len(processos),
                        "processos_condenacao_transitada": sum(1 for p in processos if p.get("status") == "transitada_em_julgado"),
                        "processos_em_andamento": sum(1 for p in processos if p.get("status") == "em_andamento"),
                        "materias_12m": len(materias),
                        "doacoes_empresas_investigadas": 0,
                        "patrimonio_declarado": sum(b.get("valor", 0) for b in bens),
                        "presenca_legislativa_percent": historico.get("presenca_percent") if historico else None,
                    }, ensure_ascii=False),
                )
            )
            candidato_id = cursor.lastrowid

            # Salvar processos
            for p in processos:
                cursor.execute(
                    """INSERT INTO secao_processos (candidato_id, tipo, instancia, status, data_inicio, data_decisao, fonte, observacao)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (candidato_id, p["tipo"], p["instancia"], p["status"],
                     p.get("data_inicio"), p.get("data_decisao"), p["fonte"], p.get("observacao"))
                )

            # Salvar matérias
            for m in materias:
                cursor.execute(
                    """INSERT INTO secao_materias (candidato_id, titulo, veiculo, data, url, fonte_api)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (candidato_id, m["titulo"], m["veiculo"], m["data"], m["url"], m.get("fonte_api"))
                )

            # Salvar gastos
            cursor.execute(
                """INSERT INTO secao_gastos_campanha (candidato_id, total_declarado, fonte)
                   VALUES (?, ?, ?)""",
                (candidato_id, contas.get("total_declarado", 0), contas.get("fonte", ""))
            )
            gasto_id = cursor.lastrowid

            # Salvar doadores (top 5)
            for d in contas.get("doadores", [])[:5]:
                cursor.execute(
                    """INSERT INTO secao_doadores (gasto_id, nome, valor, cpf_cnpj, fonte)
                       VALUES (?, ?, ?, ?, ?)""",
                    (gasto_id, d.get("nome", ""), d.get("valor", 0), d.get("cpfCnpj"), contas.get("fonte", ""))
                )

            # Salvar bens
            for b in bens:
                cursor.execute(
                    """INSERT INTO secao_bens (candidato_id, descricao, valor, tipo, fonte)
                       VALUES (?, ?, ?, ?, ?)""",
                    (candidato_id,
                     b.get("descricao", b.get("nome", "")),
                     b.get("valor", 0),
                     b.get("tipo", "Outro"),
                     "https://dadosabertos.tse.jus.br/divulgacand/2026")
                )

            # Salvar histórico legislativo
            if historico:
                cursor.execute(
                    """INSERT INTO secao_historico_legislativo (candidato_id, presenca_percent, projetos_propostos, votos_em_pautas_politicas, fonte)
                       VALUES (?, ?, ?, ?, ?)""",
                    (candidato_id, historico.get("presenca_percent"), historico.get("projetos_propostos", 0),
                     historico.get("votos_em_pautas_politicas", 0), historico.get("fonte", ""))
                )

            conn.commit()
            print(f"  ✅ Dados salvos no banco (ID: {candidato_id})")

        except Exception as e:
            print(f"  ❌ Erro ao salvar {nome}: {e}")
            conn.rollback()

    conn.close()
    print("\n" + "=" * 60)
    print("  Pipeline concluído!")
    print("=" * 60)


if __name__ == "__main__":
    init_db()
    coletar_tudo()
