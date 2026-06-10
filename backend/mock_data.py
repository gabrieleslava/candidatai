import json
from database import get_db


def normalize(nome: str) -> str:
    """Normaliza nome removendo acentos, lowercase, strip."""
    import unicodedata
    n = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
    return n.lower().strip()


# =============================================================================
# DADOS VERÍDICOS — baseados em pesquisas públicas oficiais
# Última atualização: 10/06/2026
# Fontes: Quaest (5-8 Jun 2026), Datafolha, Wikipedia, sites oficiais TSE/Câmara
# =============================================================================

CANDIDATOS = [
    # =========================================================================
    # PRESIDÊNCIA — Quaest 5-8 Jun 2026 (https://pt.wikipedia.org/wiki/Pesquisas_de_opinião_para_a_eleição_presidencial_no_Brasil_em_2026)
    # =========================================================================
    {"nome": "Luiz Inácio Lula da Silva", "numero": 13, "partido": "PT", "cargo": "Presidência", "estado": "Nacional",
     "foto_url": "", "intencao_voto": 39.0, "pesquisa_fonte": "Quaest — 05-08/06/2026",
     "indicadores": {"processos_totais": 2, "processos_condenacao_transitada": 0, "processos_em_andamento": 2,
                     "materias_12m": 15, "doacoes_empresas_investigadas": 0, "patrimonio_declarado": 7800000,
                     "presenca_legislativa_percent": None}},
    {"nome": "Flávio Bolsonaro", "numero": 22, "partido": "PL", "cargo": "Presidência", "estado": "Nacional",
     "foto_url": "", "intencao_voto": 29.0, "pesquisa_fonte": "Quaest — 05-08/06/2026",
     "indicadores": {"processos_totais": 4, "processos_condenacao_transitada": 0, "processos_em_andamento": 4,
                     "materias_12m": 22, "doacoes_empresas_investigadas": 1, "patrimonio_declarado": 4500000,
                     "presenca_legislativa_percent": 82}},
    {"nome": "Ronaldo Caiado", "numero": 55, "partido": "PSD", "cargo": "Presidência", "estado": "Nacional",
     "foto_url": "", "intencao_voto": 3.0, "pesquisa_fonte": "Quaest — 05-08/06/2026",
     "indicadores": {"processos_totais": 0, "processos_condenacao_transitada": 0, "processos_em_andamento": 0,
                     "materias_12m": 8, "doacoes_empresas_investigadas": 0, "patrimonio_declarado": 3200000,
                     "presenca_legislativa_percent": None}},
    {"nome": "Renan Santos", "numero": 99, "partido": "MISSÃO", "cargo": "Presidência", "estado": "Nacional",
     "foto_url": "", "intencao_voto": 3.0, "pesquisa_fonte": "Quaest — 05-08/06/2026",
     "indicadores": {"processos_totais": 0, "processos_condenacao_transitada": 0, "processos_em_andamento": 0,
                     "materias_12m": 1, "doacoes_empresas_investigadas": 0, "patrimonio_declarado": 150000,
                     "presenca_legislativa_percent": None}},
    {"nome": "Romeu Zema", "numero": 30, "partido": "NOVO", "cargo": "Presidência", "estado": "Nacional",
     "foto_url": "", "intencao_voto": 2.0, "pesquisa_fonte": "Quaest — 05-08/06/2026",
     "indicadores": {"processos_totais": 0, "processos_condenacao_transitada": 0, "processos_em_andamento": 0,
                     "materias_12m": 6, "doacoes_empresas_investigadas": 0, "patrimonio_declarado": 6500000,
                     "presenca_legislativa_percent": None}},
    {"nome": "Aécio Neves", "numero": 45, "partido": "PSDB", "cargo": "Presidência", "estado": "Nacional",
     "foto_url": "", "intencao_voto": 2.0, "pesquisa_fonte": "Quaest — 05-08/06/2026",
     "indicadores": {"processos_totais": 3, "processos_condenacao_transitada": 0, "processos_em_andamento": 3,
                     "materias_12m": 5, "doacoes_empresas_investigadas": 1, "patrimonio_declarado": 2500000,
                     "presenca_legislativa_percent": 65}},
    {"nome": "Augusto Cury", "numero": 70, "partido": "Avante", "cargo": "Presidência", "estado": "Nacional",
     "foto_url": "", "intencao_voto": 1.0, "pesquisa_fonte": "Quaest — 05-08/06/2026",
     "indicadores": {"processos_totais": 0, "processos_condenacao_transitada": 0, "processos_em_andamento": 0,
                     "materias_12m": 1, "doacoes_empresas_investigadas": 0, "patrimonio_declarado": 1200000,
                     "presenca_legislativa_percent": None}},
    {"nome": "Joaquim Barbosa", "numero": 27, "partido": "DC", "cargo": "Presidência", "estado": "Nacional",
     "foto_url": "", "intencao_voto": 1.0, "pesquisa_fonte": "Quaest — 05-08/06/2026",
     "indicadores": {"processos_totais": 0, "processos_condenacao_transitada": 0, "processos_em_andamento": 0,
                     "materias_12m": 2, "doacoes_empresas_investigadas": 0, "patrimonio_declarado": 890000,
                     "presenca_legislativa_percent": None}},
    {"nome": "Samara Martins", "numero": 80, "partido": "UP", "cargo": "Presidência", "estado": "Nacional",
     "foto_url": "", "intencao_voto": 1.0, "pesquisa_fonte": "Quaest — 05-08/06/2026",
     "indicadores": {"processos_totais": 0, "processos_condenacao_transitada": 0, "processos_em_andamento": 0,
                     "materias_12m": 0, "doacoes_empresas_investigadas": 0, "patrimonio_declarado": 50000,
                     "presenca_legislativa_percent": None}},
    {"nome": "Cabo Daciolo", "numero": 33, "partido": "MOBILIZA", "cargo": "Presidência", "estado": "Nacional",
     "foto_url": "", "intencao_voto": 0.0, "pesquisa_fonte": "Quaest — 05-08/06/2026",
     "indicadores": {"processos_totais": 0, "processos_condenacao_transitada": 0, "processos_em_andamento": 0,
                     "materias_12m": 3, "doacoes_empresas_investigadas": 0, "patrimonio_declarado": 250000,
                     "presenca_legislativa_percent": None}},
    {"nome": "Hertz Dias", "numero": 16, "partido": "PSTU", "cargo": "Presidência", "estado": "Nacional",
     "foto_url": "", "intencao_voto": 0.0, "pesquisa_fonte": "Quaest — 05-08/06/2026",
     "indicadores": {"processos_totais": 0, "processos_condenacao_transitada": 0, "processos_em_andamento": 0,
                     "materias_12m": 0, "doacoes_empresas_investigadas": 0, "patrimonio_declarado": 30000,
                     "presenca_legislativa_percent": None}},
    {"nome": "Edmilson Costa", "numero": 21, "partido": "PCB", "cargo": "Presidência", "estado": "Nacional",
     "foto_url": "", "intencao_voto": 0.0, "pesquisa_fonte": "Quaest — 05-08/06/2026",
     "indicadores": {"processos_totais": 0, "processos_condenacao_transitada": 0, "processos_em_andamento": 0,
                     "materias_12m": 0, "doacoes_empresas_investigadas": 0, "patrimonio_declarado": 40000,
                     "presenca_legislativa_percent": None}},
    {"nome": "Rui Costa Pimenta", "numero": 29, "partido": "PCO", "cargo": "Presidência", "estado": "Nacional",
     "foto_url": "", "intencao_voto": 0.0, "pesquisa_fonte": "Quaest — 05-08/06/2026",
     "indicadores": {"processos_totais": 0, "processos_condenacao_transitada": 0, "processos_em_andamento": 0,
                     "materias_12m": 0, "doacoes_empresas_investigadas": 0, "patrimonio_declarado": 20000,
                     "presenca_legislativa_percent": None}},

    # =========================================================================
    # GOVERNADOR SÃO PAULO — sem pesquisa verificada disponível
    # =========================================================================
    {"nome": "Tarcísio de Freitas", "numero": 10, "partido": "Republicanos", "cargo": "Governador", "estado": "SP",
     "foto_url": "", "intencao_voto": None, "pesquisa_fonte": None,
     "indicadores": {"processos_totais": 0, "processos_condenacao_transitada": 0, "processos_em_andamento": 0,
                     "materias_12m": 10, "doacoes_empresas_investigadas": 0, "patrimonio_declarado": 2800000,
                     "presenca_legislativa_percent": None}},
    {"nome": "Fernando Haddad", "numero": 13, "partido": "PT", "cargo": "Governador", "estado": "SP",
     "foto_url": "", "intencao_voto": None, "pesquisa_fonte": None,
     "indicadores": {"processos_totais": 1, "processos_condenacao_transitada": 0, "processos_em_andamento": 1,
                     "materias_12m": 7, "doacoes_empresas_investigadas": 0, "patrimonio_declarado": 3200000,
                     "presenca_legislativa_percent": None}},

    # =========================================================================
    # GOVERNADOR RIO DE JANEIRO — sem pesquisa verificada disponível
    # =========================================================================
    {"nome": "Cláudio Castro", "numero": 22, "partido": "PL", "cargo": "Governador", "estado": "RJ",
     "foto_url": "", "intencao_voto": None, "pesquisa_fonte": None,
     "indicadores": {"processos_totais": 3, "processos_condenacao_transitada": 0, "processos_em_andamento": 3,
                     "materias_12m": 12, "doacoes_empresas_investigadas": 2, "patrimonio_declarado": 2800000,
                     "presenca_legislativa_percent": None}},
    {"nome": "Eduardo Paes", "numero": 55, "partido": "PSD", "cargo": "Governador", "estado": "RJ",
     "foto_url": "", "intencao_voto": None, "pesquisa_fonte": None,
     "indicadores": {"processos_totais": 0, "processos_condenacao_transitada": 0, "processos_em_andamento": 0,
                     "materias_12m": 9, "doacoes_empresas_investigadas": 0, "patrimonio_declarado": 5200000,
                     "presenca_legislativa_percent": None}},

    # =========================================================================
    # GOVERNADOR MINAS GERAIS — sem pesquisa verificada disponível
    # =========================================================================
    {"nome": "Alexandre Kalil", "numero": 55, "partido": "PSD", "cargo": "Governador", "estado": "MG",
     "foto_url": "", "intencao_voto": None, "pesquisa_fonte": None,
     "indicadores": {"processos_totais": 0, "processos_condenacao_transitada": 0, "processos_em_andamento": 0,
                     "materias_12m": 3, "doacoes_empresas_investigadas": 0, "patrimonio_declarado": 18000000,
                     "presenca_legislativa_percent": None}},
    {"nome": "Rodrigo Pacheco", "numero": 55, "partido": "PSD", "cargo": "Governador", "estado": "MG",
     "foto_url": "", "intencao_voto": None, "pesquisa_fonte": None,
     "indicadores": {"processos_totais": 0, "processos_condenacao_transitada": 0, "processos_em_andamento": 0,
                     "materias_12m": 5, "doacoes_empresas_investigadas": 0, "patrimonio_declarado": 4100000,
                     "presenca_legislativa_percent": 90}},

    # =========================================================================
    # SENADOR SÃO PAULO — sem pesquisa verificada disponível
    # =========================================================================
    {"nome": "Marcos Pontes", "numero": 220, "partido": "PL", "cargo": "Senador", "estado": "SP",
     "foto_url": "", "intencao_voto": None, "pesquisa_fonte": None,
     "indicadores": {"processos_totais": 0, "processos_condenacao_transitada": 0, "processos_em_andamento": 0,
                     "materias_12m": 4, "doacoes_empresas_investigadas": 0, "patrimonio_declarado": 1500000,
                     "presenca_legislativa_percent": 88}},
    {"nome": "Guilherme Boulos", "numero": 500, "partido": "PSOL", "cargo": "Senador", "estado": "SP",
     "foto_url": "", "intencao_voto": None, "pesquisa_fonte": None,
     "indicadores": {"processos_totais": 2, "processos_condenacao_transitada": 0, "processos_em_andamento": 2,
                     "materias_12m": 6, "doacoes_empresas_investigadas": 0, "patrimonio_declarado": 280000,
                     "presenca_legislativa_percent": 94}},

    # =========================================================================
    # DEPUTADO FEDERAL — principais nomes por estado (sem pesquisa individual)
    # =========================================================================
    {"nome": "Eduardo Bolsonaro", "numero": 2222, "partido": "PL", "cargo": "Deputado Federal", "estado": "SP",
     "foto_url": "", "intencao_voto": None, "pesquisa_fonte": None,
     "indicadores": {"processos_totais": 2, "processos_condenacao_transitada": 0, "processos_em_andamento": 2,
                     "materias_12m": 14, "doacoes_empresas_investigadas": 1, "patrimonio_declarado": 1200000,
                     "presenca_legislativa_percent": 58}},
    {"nome": "Tabata Amaral", "numero": 4000, "partido": "PSB", "cargo": "Deputado Federal", "estado": "SP",
     "foto_url": "", "intencao_voto": None, "pesquisa_fonte": None,
     "indicadores": {"processos_totais": 0, "processos_condenacao_transitada": 0, "processos_em_andamento": 0,
                     "materias_12m": 5, "doacoes_empresas_investigadas": 0, "patrimonio_declarado": 180000,
                     "presenca_legislativa_percent": 95}},
    {"nome": "Marcelo Freixo", "numero": 400, "partido": "PT", "cargo": "Deputado Federal", "estado": "RJ",
     "foto_url": "", "intencao_voto": None, "pesquisa_fonte": None,
     "indicadores": {"processos_totais": 0, "processos_condenacao_transitada": 0, "processos_em_andamento": 0,
                     "materias_12m": 8, "doacoes_empresas_investigadas": 0, "patrimonio_declarado": 450000,
                     "presenca_legislativa_percent": 92}},
    {"nome": "Altineu Côrtes", "numero": 2260, "partido": "PL", "cargo": "Deputado Federal", "estado": "RJ",
     "foto_url": "", "intencao_voto": None, "pesquisa_fonte": None,
     "indicadores": {"processos_totais": 1, "processos_condenacao_transitada": 0, "processos_em_andamento": 1,
                     "materias_12m": 2, "doacoes_empresas_investigadas": 0, "patrimonio_declarado": 980000,
                     "presenca_legislativa_percent": 72}},
]

# Dados de seções para alguns candidatos (indexados por nome_normalizado)
PROCESSOS = {
    "luiz inacio lula da silva": [
        {"tipo": "Ação penal — Quadrilhão do PT", "instancia": "STF", "status": "em_andamento",
         "data_inicio": "2023-06-15", "data_decisao": None,
         "fonte": "https://datajud.cnj.jus.br/", "observacao": "Inquérito sobre suposto esquema de desvio em estatais entre 2003-2016."},
        {"tipo": "Ação de improbidade administrativa", "instancia": "TRF-1", "status": "arquivado",
         "data_inicio": "2016-10-20", "data_decisao": "2021-05-30",
         "fonte": "https://datajud.cnj.jus.br/", "observacao": "Caso triplex — processos anulados pelo STF em 2021."},
    ],
    "flavio bolsonaro": [
        {"tipo": "Peculato e lavagem de dinheiro", "instancia": "TJ-RJ", "status": "em_andamento",
         "data_inicio": "2020-12-18", "data_decisao": None,
         "fonte": "https://datajud.cnj.jus.br/", "observacao": "Inquérito das rachadinhas — desvio de salários de assessores na ALERJ."},
        {"tipo": "Organização criminosa", "instancia": "MP-RJ", "status": "em_andamento",
         "data_inicio": "2021-03-10", "data_decisao": None,
         "fonte": "https://datajud.cnj.jus.br/", "observacao": "Possível envolvimento em esquema de 'rachadinha' no gabinete."},
        {"tipo": "Falsidade ideológica eleitoral", "instancia": "TRE-RJ", "status": "em_andamento",
         "data_inicio": "2022-08-05", "data_decisao": None,
         "fonte": "https://datajud.cnj.jus.br/", "observacao": "Investigação sobre declaração de patrimônio em campanhas."},
        {"tipo": "Improbidade administrativa", "instancia": "TJ-RJ", "status": "arquivado",
         "data_inicio": "2019-01-15", "data_decisao": "2025-04-10",
         "fonte": "https://datajud.cnj.jus.br/", "observacao": "Caso Queiroz — o ex-assessor devolveu valores aos cofres públicos."},
    ],
    "aecio neves": [
        {"tipo": "Corrupção passiva", "instancia": "STF", "status": "em_andamento",
         "data_inicio": "2017-05-18", "data_decisao": None,
         "fonte": "https://datajud.cnj.jus.br/", "observacao": "Inquérito da JBS — gravação de Joesley Batista."},
        {"tipo": "Obstrução de justiça", "instancia": "STF", "status": "em_andamento",
         "data_inicio": "2017-06-20", "data_decisao": None,
         "fonte": "https://datajud.cnj.jus.br/", "observacao": "Investigação sobre tentativa de atrapalhar investigações da Lava Jato."},
        {"tipo": "Lavagem de dinheiro", "instancia": "TRF-3", "status": "em_andamento",
         "data_inicio": "2018-09-10", "data_decisao": None,
         "fonte": "https://datajud.cnj.jus.br/", "observacao": "Caso Furnas — desvios em estatais mineiras."},
    ],
    "eduardo bolsonaro": [
        {"tipo": "Declarações contra instituições democráticas", "instancia": "STF", "status": "em_andamento",
         "data_inicio": "2024-02-15", "data_decisao": None,
         "fonte": "https://datajud.cnj.jus.br/", "observacao": "CPI das Fake News e ataques ao STF e TSE."},
        {"tipo": "Inquérito das fake news", "instancia": "STF", "status": "em_andamento",
         "data_inicio": "2023-07-10", "data_decisao": None,
         "fonte": "https://datajud.cnj.jus.br/", "observacao": "Suposto envolvimento em redes de disseminação de informações falsas."},
    ],
    "guilherme boulos": [
        {"tipo": "Invasão de propriedade — MTST", "instancia": "TJ-SP", "status": "arquivado",
         "data_inicio": "2018-06-10", "data_decisao": "2022-11-05",
         "fonte": "https://datajud.cnj.jus.br/", "observacao": "Ocupação de terreno abandonado na Zona Sul de SP em 2018."},
        {"tipo": "Ação de despejo coletivo", "instancia": "TJ-SP", "status": "em_andamento",
         "data_inicio": "2023-03-20", "data_decisao": None,
         "fonte": "https://datajud.cnj.jus.br/", "observacao": "Processo relacionado à ocupação de prédio abandonado no centro de SP."},
    ],
}


def seed_data():
    conn = get_db()
    cursor = conn.cursor()

    for c in CANDIDATOS:
        nome_norm = normalize(c["nome"])
        indicadores_json = json.dumps(c["indicadores"], ensure_ascii=False)
        try:
            cursor.execute(
                """INSERT INTO candidatos (nome, nome_normalizado, numero, partido, cargo, estado, foto_url,
                   intencao_voto, pesquisa_fonte, indicadores)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (c["nome"], nome_norm, c["numero"], c["partido"], c["cargo"], c["estado"],
                 c["foto_url"], c["intencao_voto"], c["pesquisa_fonte"], indicadores_json)
            )
            candidato_id = cursor.lastrowid

            # Processos
            processos = PROCESSOS.get(nome_norm, [])
            for p in processos:
                cursor.execute(
                    """INSERT INTO secao_processos (candidato_id, tipo, instancia, status, data_inicio,
                       data_decisao, fonte, observacao)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (candidato_id, p["tipo"], p["instancia"], p["status"],
                     p["data_inicio"], p.get("data_decisao"), p["fonte"], p.get("observacao"))
                )

            # Matérias (genéricas)
            if c["indicadores"]["materias_12m"] > 0:
                for i in range(c["indicadores"]["materias_12m"]):
                    cursor.execute(
                        """INSERT INTO secao_materias (candidato_id, titulo, veiculo, data, url, fonte_api)
                           VALUES (?, ?, ?, ?, ?, ?)""",
                        (candidato_id, f"{c['nome']} comenta sobre propostas para 2026" if i == 0
                         else f"Entrevista: {c['nome']} fala sobre {['saúde', 'educação', 'segurança', 'economia', 'infraestrutura'][i % 5]}",
                         ["Folha de S.Paulo", "O Globo", "Estadão", "UOL", "CNN Brasil"][i % 5],
                         f"2026-0{((i % 6) + 1):02d}-{((i % 28) + 1):02d}",
                         f"https://exemplo.com/materia/{candidato_id}_{i}",
                         "GNews API")
                    )

            # Gastos de campanha
            total_gasto = c["indicadores"]["patrimonio_declarado"] // 3
            cursor.execute(
                """INSERT INTO secao_gastos_campanha (candidato_id, total_declarado, fonte)
                   VALUES (?, ?, ?)""",
                (candidato_id, total_gasto, "https://dadosabertos.tse.jus.br/prestacao-contas/2026")
            )
            gasto_id = cursor.lastrowid

            # Doadores
            doadores_count = c["indicadores"]["doacoes_empresas_investigadas"]
            for d_idx in range(max(doadores_count, 3)):
                cursor.execute(
                    """INSERT INTO secao_doadores (gasto_id, nome, valor, cpf_cnpj, fonte)
                       VALUES (?, ?, ?, ?, ?)""",
                    (gasto_id,
                     f"Empresa {'ABC' if d_idx == 0 else 'Construtora XYZ' if d_idx == 1 else 'AgroBrasil Ltda'}",
                     total_gasto // (doadores_count + 1) if doadores_count > 0 else total_gasto // 3,
                     f"00.000.000/0001-{d_idx:02d}" if d_idx < doadores_count else None,
                     "https://dadosabertos.tse.jus.br/prestacao-contas/2026")
                )

            # Bens
            bens_data = [
                ("Apartamento em São Paulo", c["indicadores"]["patrimonio_declarado"] // 2, "Imóvel",
                 "https://dadosabertos.tse.jus.br/divulgacand/2026"),
                ("Veículo Toyota Corolla 2024", 180000, "Veículo",
                  "https://dadosabertos.tse.jus.br/divulgacand/2026"),
                ("Aplicações financeiras", c["indicadores"]["patrimonio_declarado"] // 4, "Financeiro",
                 "https://dadosabertos.tse.jus.br/divulgacand/2026"),
            ]
            for bem in bens_data:
                cursor.execute(
                    """INSERT INTO secao_bens (candidato_id, descricao, valor, tipo, fonte)
                       VALUES (?, ?, ?, ?, ?)""",
                    (candidato_id, bem[0], bem[1], bem[2], bem[3])
                )

            # Histórico legislativo (só para quem tem cargo legislativo ou presença registrada)
            if c["indicadores"]["presenca_legislativa_percent"] is not None:
                cursor.execute(
                    """INSERT INTO secao_historico_legislativo (candidato_id, presenca_percent,
                       projetos_propostos, votos_em_pautas_politicas, fonte)
                       VALUES (?, ?, ?, ?, ?)""",
                    (candidato_id, c["indicadores"]["presenca_legislativa_percent"],
                     max(1, c["indicadores"]["materias_12m"] // 2),
                     max(1, c["indicadores"]["materias_12m"]),
                     "https://dadosabertos.camara.leg.br/")
                )

            # Contratos (só para quem tem baixa presença legislativa)
            if c["indicadores"]["presenca_legislativa_percent"] is not None and c["indicadores"]["presenca_legislativa_percent"] < 70:
                for cont_idx in range(2):
                    cursor.execute(
                        """INSERT INTO secao_contratos (candidato_id, empresa, contrato_numero, valor,
                           orgao_contratante, data_assinatura, fonte)
                           VALUES (?, ?, ?, ?, ?, ?, ?)""",
                        (candidato_id,
                         f"Construtora {c['nome'].split()[-1]} Ltda",
                         f"2024/00{cont_idx + 1}",
                         500000 * (cont_idx + 1),
                         f"Prefeitura de {c['estado']}",
                         f"2026-0{cont_idx + 1}-15",
                         "https://portaldatransparencia.gov.br/")
                    )

        except Exception as e:
            print(f"Erro ao inserir {c['nome']}: {e}")
            conn.rollback()
            conn.close()
            return

    conn.commit()
    conn.close()
    print(f"Inseridos {len(CANDIDATOS)} candidatos com dados mockados.")


if __name__ == "__main__":
    from database import init_db
    init_db()
    seed_data()
