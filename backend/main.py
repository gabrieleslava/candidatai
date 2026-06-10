import json
import os
from typing import Optional
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_db, init_db
from mock_data import seed_data, normalize
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


def row_to_dict(row):
    if row is None:
        return None
    return dict(row)


@app.on_event("startup")
def startup():
    if not os.path.exists(DB_PATH):
        init_db()
        seed_data()

    # Tentar enriquecer com dados reais (não bloqueante)
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

        # Aplicar filtros de evidências
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
            perfil = perfil_candidato(cid)
            resultados.append(perfil)
        except HTTPException:
            pass

    return resultados


@app.get("/api/candidatos/{candidato_id}")
def perfil_candidato(candidato_id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM candidatos WHERE id = ?", (candidato_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Candidato não encontrado")

    c = dict(row)
    c["indicadores"] = json.loads(c["indicadores"])

    # Processos
    cursor.execute("SELECT * FROM secao_processos WHERE candidato_id = ? ORDER BY data_inicio DESC", (candidato_id,))
    processos = [dict(r) for r in cursor.fetchall()]

    # Matérias
    cursor.execute("SELECT * FROM secao_materias WHERE candidato_id = ? ORDER BY data DESC", (candidato_id,))
    materias = [dict(r) for r in cursor.fetchall()]

    # Gastos
    cursor.execute("SELECT * FROM secao_gastos_campanha WHERE candidato_id = ?", (candidato_id,))
    gasto_row = cursor.fetchone()
    gastos = None
    doadores = []
    if gasto_row:
        gasto_dict = dict(gasto_row)
        cursor.execute("SELECT * FROM secao_doadores WHERE gasto_id = ?", (gasto_dict["id"],))
        doadores = [dict(r) for r in cursor.fetchall()]
        gastos = {
            "total_declarado": gasto_dict["total_declarado"],
            "maiores_doadores": doadores,
            "fonte": gasto_dict["fonte"],
        }

    # Bens
    cursor.execute("SELECT * FROM secao_bens WHERE candidato_id = ?", (candidato_id,))
    bens = [dict(r) for r in cursor.fetchall()]

    # Histórico legislativo
    cursor.execute("SELECT * FROM secao_historico_legislativo WHERE candidato_id = ?", (candidato_id,))
    hl_row = cursor.fetchone()
    historico = dict(hl_row) if hl_row else None

    # Contratos
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
    """Retorna status das integrações com APIs externas."""
    import requests
    status = {
        "camara": "unavailable",
        "tse": "unavailable",
        "datajud": "unavailable",
        "gnews": "unavailable",
    }

    # Testar Câmara
    try:
        r = requests.get("https://dadosabertos.camara.leg.br/api/v2/deputados?itens=1", timeout=5)
        status["camara"] = "ok" if r.status_code == 200 else f"error_{r.status_code}"
    except Exception as e:
        status["camara"] = str(e)

    # Testar Portal da Transparência
    try:
        r = requests.get(
            "https://api.portaldatransparencia.gov.br/api-de-dados/orgaos-siafi?pagina=1",
            headers={"chave-api-dados": os.environ.get("PORTAL_TRANSPARENCIA_TOKEN", "")},
            timeout=10,
        )
        status["portal_transparencia"] = "ok" if r.status_code == 200 else f"error_{r.status_code}"
    except Exception as e:
        status["portal_transparencia"] = str(e)

    # Testar TSE (provavelmente indisponível até registro de candidaturas)
    try:
        r = requests.get("https://dadosabertos.tse.jus.br/api/v2/", timeout=5)
        status["tse"] = "ok" if r.status_code == 200 else f"error_{r.status_code}"
    except Exception as e:
        status["tse"] = str(e)

    # Testar GNews
    try:
        gnews_key = os.environ.get("GNEWS_API_KEY", "")
        if gnews_key:
            r = requests.get(
                f"https://gnews.io/api/v4/search?q=teste&max=1&token={gnews_key}",
                timeout=5,
            )
            status["gnews"] = "ok" if r.status_code in (200, 401, 403) else f"error_{r.status_code}"
        else:
            status["gnews"] = "unconfigured"
    except Exception as e:
        status["gnews"] = str(e)

    return {
        "integracoes": status,
        "modo": "hibrido",
        "observacao": "Dados mockados enriquecidos com APIs disponíveis. TSE 2026 disponível após registro de candidaturas (agosto/2026).",
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
