"""
Pipeline híbrido: usa APIs disponíveis + fallback para mock.
- Câmara dos Deputados: histórico legislativo real ✅
- TSE/DataJud: preparados, usarão mock até estarem disponíveis
"""
import json
import os
from database import get_db, init_db
from mock_data import seed_data, normalize
from collectors.camara_collector import obter_historico_legislativo
from collectors.news_collector import buscar_materias_candidato, buscar_materias_candidato_fallback


def enriquecer_com_dados_reais():
    """
    Inicia com dados mockados e enriquece com dados reais das APIs disponíveis.
    """
    print("=" * 60)
    print("  CandidatAI — Pipeline Híbrido de Coleta")
    print("=" * 60)

    conn = get_db()
    cursor = conn.cursor()

    # Buscar todos os candidatos do banco (mock)
    cursor.execute("SELECT id, nome, cargo FROM candidatos")
    candidatos = cursor.fetchall()

    total = len(candidatos)
    print(f"\n  {total} candidatos no banco. Enriquecendo com dados reais...")

    for idx, c in enumerate(candidatos):
        nome = c["nome"]
        cargo = c["cargo"]
        candidato_id = c["id"]

        print(f"\n[{idx + 1}/{total}] {nome} ({cargo})")

        # 1. Histórico legislativo (Câmara) — apenas para deputados federais e senadores
        if cargo in ("Deputado Federal", "Senador", "Deputado Estadual"):
            print("  → Buscando histórico legislativo na Câmara...")
            historico = obter_historico_legislativo(nome)
            if historico:
                cursor.execute(
                    """INSERT OR REPLACE INTO secao_historico_legislativo
                       (candidato_id, presenca_percent, projetos_propostos, votos_em_pautas_politicas, fonte)
                       VALUES (?, ?, ?, ?, ?)""",
                    (candidato_id, historico["presenca_percent"],
                     historico["projetos_propostos"], historico["votos_em_pautas_politicas"],
                     historico["fonte"])
                )
                # Atualizar indicadores
                cursor.execute("SELECT indicadores FROM candidatos WHERE id = ?", (candidato_id,))
                row = cursor.fetchone()
                if row:
                    indicadores = json.loads(row["indicadores"])
                    if historico["presenca_percent"] is not None:
                        indicadores["presenca_legislativa_percent"] = historico["presenca_percent"]
                    indicadores["projetos_propostos"] = historico["projetos_propostos"]
                    cursor.execute("UPDATE candidatos SET indicadores = ? WHERE id = ?",
                                   (json.dumps(indicadores, ensure_ascii=False), candidato_id))
                print(f"    ✅ Histórico legislativo atualizado ({historico['projetos_propostos']} projetos)")
            else:
                print("    ⚠️ Não encontrado na Câmara")

        # 2. Matérias na mídia (GNews/NewsAPI)
        print("  → Buscando matérias na mídia...")
        materias = buscar_materias_candidato(nome) or buscar_materias_candidato_fallback(nome) or []
        if materias:
            for m in materias:
                cursor.execute(
                    """INSERT INTO secao_materias (candidato_id, titulo, veiculo, data, url, fonte_api)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (candidato_id, m["titulo"], m["veiculo"], m["data"], m["url"], m.get("fonte_api", ""))
                )
            print(f"    ✅ {len(materias)} matérias adicionadas")
        else:
            print("    ⚠️ Nenhuma matéria encontrada (API key não configurada?)")

        conn.commit()

    conn.close()
    print("\n" + "=" * 60)
    print("  Enriquecimento concluído!")
    print("=" * 60)


if __name__ == "__main__":
    if not os.path.exists("candidatai.db"):
        print("Banco não existe. Inicializando com dados mock...")
        init_db()
        seed_data()
    enriquecer_com_dados_reais()
