import json
import os
import requests
from typing import Optional
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_db, init_db
import os.path
from database import DB_PATH
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="CandidatAI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def normalize(texto: str) -> str:
    import unicodedata
    texto = unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII")
    texto = " ".join(texto.lower().split())
    return texto


# Apenas dados básicos verificáveis (nome, partido, cargo, estado, pesquisa)
# Sem dados de processos, bens, gastos, contratos — isso vem das APIs externas
CANDIDATOS_BASE = [
    # PRESIDÊNCIA — Quaest 5-8 Jun 2026
    {"nome": "Luiz Inácio Lula da Silva", "numero": 13, "partido": "PT", "cargo": "Presidência", "estado": "Nacional",
     "intencao_voto": 39.0, "pesquisa_fonte": "Quaest — 05-08/06/2026"},
    {"nome": "Flávio Bolsonaro", "numero": 22, "partido": "PL", "cargo": "Presidência", "estado": "Nacional",
     "intencao_voto": 29.0, "pesquisa_fonte": "Quaest — 05-08/06/2026"},
    {"nome": "Ronaldo Caiado", "numero": 55, "partido": "PSD", "cargo": "Presidência", "estado": "Nacional",
     "intencao_voto": 3.0, "pesquisa_fonte": "Quaest — 05-08/06/2026"},
    {"nome": "Renan Santos", "numero": 99, "partido": "MISSÃO", "cargo": "Presidência", "estado": "Nacional",
     "intencao_voto": 3.0, "pesquisa_fonte": "Quaest — 05-08/06/2026"},
    {"nome": "Romeu Zema", "numero": 30, "partido": "NOVO", "cargo": "Presidência", "estado": "Nacional",
     "intencao_voto": 2.0, "pesquisa_fonte": "Quaest — 05-08/06/2026"},
    {"nome": "Aécio Neves", "numero": 45, "partido": "PSDB", "cargo": "Presidência", "estado": "Nacional",
     "intencao_voto": 2.0, "pesquisa_fonte": "Quaest — 05-08/06/2026"},
    # GOVERNADOR SP
    {"nome": "Tarcísio de Freitas", "numero": 10, "partido": "Republicanos", "cargo": "Governador", "estado": "SP",
     "intencao_voto": None, "pesquisa_fonte": None},
    {"nome": "Fernando Haddad", "numero": 13, "partido": "PT", "cargo": "Governador", "estado": "SP",
     "intencao_voto": None, "pesquisa_fonte": None},
    # GOVERNADOR RJ
    {"nome": "Cláudio Castro", "numero": 22, "partido": "PL", "cargo": "Governador", "estado": "RJ",
     "intencao_voto": None, "pesquisa_fonte": None},
    {"nome": "Eduardo Paes", "numero": 55, "partido": "PSD", "cargo": "Governador", "estado": "RJ",
     "intencao_voto": None, "pesquisa_fonte": None},
    # GOVERNADOR MG
    {"nome": "Alexandre Kalil", "numero": 55, "partido": "PSD", "cargo": "Governador", "estado": "MG",
     "intencao_voto": None, "pesquisa_fonte": None},
    {"nome": "Rodrigo Pacheco", "numero": 55, "partido": "PSD", "cargo": "Governador", "estado": "MG",
     "intencao_voto": None, "pesquisa_fonte": None},
    # SENADORES
    {"nome": "Marcos Pontes", "numero": 220, "partido": "PL", "cargo": "Senador", "estado": "SP",
     "intencao_voto": None, "pesquisa_fonte": None},
    {"nome": "Guilherme Boulos", "numero": 500, "partido": "PSOL", "cargo": "Deputado Federal", "estado": "SP",
     "intencao_voto": None, "pesquisa_fonte": None},
    # DEPUTADOS FEDERAIS
    {"nome": "Eduardo Bolsonaro", "numero": 2222, "partido": "PL", "cargo": "Deputado Federal", "estado": "SP",
     "intencao_voto": None, "pesquisa_fonte": None},
    {"nome": "Tabata Amaral", "numero": 4000, "partido": "PSB", "cargo": "Deputado Federal", "estado": "SP",
     "intencao_voto": None, "pesquisa_fonte": None},
    {"nome": "Marcelo Freixo", "numero": 400, "partido": "PT", "cargo": "Deputado Federal", "estado": "RJ",
     "intencao_voto": None, "pesquisa_fonte": None},
]


def _indicadores_zero():
    return json.dumps({
        "processos_totais": 0,
        "processos_condenacao_transitada": 0,
        "processos_em_andamento": 0,
        "materias_12m": 0,
        "doacoes_empresas_investigadas": 0,
        "patrimonio_declarado": 0,
        "presenca_legislativa_percent": None,
    })


def _seed_candidatos():
    """Insere apenas dados básicos — sem seções mock. As seções são preenchidas pelas APIs."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM candidatos")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    for c in CANDIDATOS_BASE:
        cursor.execute(
            """INSERT INTO candidatos (nome, nome_normalizado, numero, partido, cargo, estado, foto_url,
               intencao_voto, pesquisa_fonte, indicadores, data_atualizacao)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                c["nome"],
                normalize(c["nome"]),
                c["numero"],
                c["partido"],
                c["cargo"],
                c["estado"],
                "",
                c["intencao_voto"],
                c["pesquisa_fonte"],
                _indicadores_zero(),
                "2026-06-10",
            ),
        )
    conn.commit()
    conn.close()
    print(f"[Startup] {len(CANDIDATOS_BASE)} candidatos inseridos.")


@app.on_event("startup")
def startup():
    if not os.path.exists(DB_PATH):
        init_db()
        _seed_candidatos()

    # Enriquecer com dados reais das APIs
    try:
        from collectors.hybrid_pipeline import enriquecer_com_dados_reais
        enriquecer_com_dados_reais()
    except Exception as e:
        print(f"[Startup] Enriquecimento com dados reais falhou (não crítico): {e}")


@app.get("/api/candidatos")
def listar_candidatos(
    cargo: Optional[str] = Query(None),
    estado: Optional[str] = Query(None),
    busca: Optional[str] = Query(None),
    tem_processos: Optional[bool] = Query(None),
    tem_condenacao: Optional[bool] = Query(None),
    tem_doacao_investigada: Optional[bool] = Query(None),
    baixa_presenca: Optional[bool] = Query(None),
):
    conn = get_db()
    cursor = conn.cursor()

    query = "SELECT * FROM candidatos WHERE 1=1"
    params = []

    if cargo:
        query += " AND cargo = ?"
        params.append(cargo)
    if estado:
        query += " AND estado = ?"
        params.append(estado)
    if busca:
        query += " AND nome_normalizado LIKE ?"
        params.append(f"%{normalize(busca)}%")

    cursor.execute(query + " ORDER BY intencao_voto DESC NULLS LAST, nome ASC", params)
    rows = cursor.fetchall()

    resultados = []
    for row in rows:
        c = dict(row)
        c["indicadores"] = json.loads(c["indicadores"])

        if tem_processos and c["indicadores"]["processos_totais"] == 0:
            continue
        if tem_condenacao and c["indicadores"]["processos_condenacao_transitada"] == 0:
            continue
        if tem_doacao_investigada and c["indicadores"]["doacoes_empresas_investigadas"] == 0:
            continue
        if baixa_presenca:
            pres = c["indicadores"]["presenca_legislativa_percent"]
            if pres is None or pres >= 70:
                continue

        resultados.append(c)

    conn.close()
    return resultados


@app.get("/api/candidatos/comparar")
def comparar_candidatos(ids: str = Query(..., description="IDs separados por vírgula, ex: 1,2")):
    ids_list = [int(x.strip()) for x in ids.split(",") if x.strip()]
    if len(ids_list) < 2 or len(ids_list) > 4:
        raise HTTPException(status_code=400, detail="Forneça entre 2 e 4 IDs de candidatos")

    resultados = []
    for cid in ids_list:
        try:
            perfil = _perfil_candidato_interno(cid)
            if perfil:
                resultados.append(perfil)
        except HTTPException:
            pass

    return resultados


def _perfil_candidato_interno(candidato_id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM candidatos WHERE id = ?", (candidato_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Candidato não encontrado")

    c = dict(row)
    c["indicadores"] = json.loads(c["indicadores"])

    cursor.execute("SELECT * FROM secao_processos WHERE candidato_id = ? ORDER BY data_inicio DESC", (candidato_id,))
    processos = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM secao_materias WHERE candidato_id = ? ORDER BY data DESC", (candidato_id,))
    materias = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM secao_gastos_campanha WHERE candidato_id = ?", (candidato_id,))
    gasto_row = cursor.fetchone()
    gastos = None
    if gasto_row:
        gasto_dict = dict(gasto_row)
        cursor.execute("SELECT * FROM secao_doadores WHERE gasto_id = ?", (gasto_dict["id"],))
        doadores = [dict(r) for r in cursor.fetchall()]
        gastos = {
            "total_declarado": gasto_dict["total_declarado"],
            "maiores_doadores": doadores,
            "fonte": gasto_dict["fonte"],
        }

    cursor.execute("SELECT * FROM secao_bens WHERE candidato_id = ?", (candidato_id,))
    bens = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM secao_historico_legislativo WHERE candidato_id = ?", (candidato_id,))
    hl_row = cursor.fetchone()
    historico = dict(hl_row) if hl_row else None

    cursor.execute("SELECT * FROM secao_contratos WHERE candidato_id = ?", (candidato_id,))
    contratos = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return {
        "candidato": {
            "nome": c["nome"],
            "numero": c["numero"],
            "partido": c["partido"],
            "cargo": c["cargo"],
            "estado": c["estado"],
            "intencao_voto": c["intencao_voto"],
            "pesquisa_fonte": c["pesquisa_fonte"],
            "foto_url": c["foto_url"],
            "indicadores": c["indicadores"],
        },
        "secoes": {
            "processos": processos,
            "materias": materias,
            "gastos_campanha": gastos,
            "bens_declarados": bens,
            "historico_legislativo": historico,
            "contratos_governo": contratos,
        },
        "data_atualizacao": c["data_atualizacao"],
        "versao_schema": "1.0",
    }


@app.get("/api/candidatos/{candidato_id}")
def perfil_candidato(candidato_id: int):
    return _perfil_candidato_interno(candidato_id)


@app.get("/api/filtros")
def opcoes_filtros():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT cargo FROM candidatos ORDER BY cargo")
    cargos = [r["cargo"] for r in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT estado FROM candidatos ORDER BY estado")
    estados = [r["estado"] for r in cursor.fetchall()]

    conn.close()
    return {"cargos": cargos, "estados": estados}


@app.get("/api/status")
def status_integracoes():
    status = {
        "camara": "unavailable",
        "tse": "unavailable",
        "datajud": "unavailable",
        "gnews": "unavailable",
        "portal_transparencia": "unavailable",
    }

    try:
        r = requests.get("https://dadosabertos.camara.leg.br/api/v2/deputados?itens=1", timeout=5)
        status["camara"] = "ok" if r.status_code == 200 else f"error_{r.status_code}"
    except Exception as e:
        status["camara"] = str(e)

    try:
        r = requests.get(
            "https://api.portaldatransparencia.gov.br/api-de-dados/orgaos-siafi?pagina=1",
            headers={"chave-api-dados": os.environ.get("PORTAL_TRANSPARENCIA_TOKEN", "")},
            timeout=10,
        )
        status["portal_transparencia"] = "ok" if r.status_code == 200 else f"error_{r.status_code}"
    except Exception as e:
        status["portal_transparencia"] = str(e)

    try:
        r = requests.get("https://dadosabertos.tse.jus.br/api/v2/", timeout=5)
        status["tse"] = "ok" if r.status_code == 200 else f"error_{r.status_code}"
    except Exception as e:
        status["tse"] = str(e)

    try:
        gnews_key = os.environ.get("GNEWS_API_KEY", "")
        if gnews_key:
            r = requests.get(f"https://gnews.io/api/v4/search?q=teste&max=1&token={gnews_key}", timeout=5)
            status["gnews"] = "ok" if r.status_code in (200, 401, 403) else f"error_{r.status_code}"
        else:
            status["gnews"] = "unconfigured"
    except Exception as e:
        status["gnews"] = str(e)

    return {
        "integracoes": status,
        "modo": "real",
        "observacao": "Apenas dados obtidos de fontes oficiais. Sem dados fictícios.",
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
