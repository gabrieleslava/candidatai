"""
Coletor Câmara dos Deputados — Histórico Legislativo
API REST: https://dadosabertos.camara.leg.br/api/v2/

Endpoints:
- /deputados — lista de deputados
- /deputados/{id} — detalhes + presença
- /deputados/{id}/proposicoes — projetos propostos
- /votacoes — votações
"""
import requests

CAMARA_BASE = "https://dadosabertos.camara.leg.br/api/v2"

HEADERS = {
    "User-Agent": "CandidatAI/1.0 (painel-transparencia; contato@exemplo.com)",
    "Accept": "application/json",
}


def buscar_deputados_por_nome(nome: str):
    """Busca deputado por nome na API da Câmara."""
    url = f"{CAMARA_BASE}/deputados"
    params = {"nome": nome, "ordem": "ASC", "ordenarPor": "nome"}
    try:
        resp = requests.get(url, params=params, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("dados", [])
    except requests.RequestException as e:
        print(f"[Câmara] Erro ao buscar deputado '{nome}': {e}")
        return []


def buscar_presenca_deputado(deputado_id: int):
    """Busca presença de um deputado nas votações."""
    url = f"{CAMARA_BASE}/deputados/{deputado_id}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        deputado = data.get("dados", {})
        ultimo_status = deputado.get("ultimoStatus", {})
        return {
            "presenca_percent": None,  # precisa de endpoint específico
            "projetos_propostos": 0,
            "votos_em_pautas_politicas": 0,
        }
    except requests.RequestException as e:
        print(f"[Câmara] Erro ao buscar presença do deputado {deputado_id}: {e}")
        return None


def buscar_proposicoes_deputado(deputado_id: int):
    """Busca proposições (projetos de lei) de um deputado."""
    url = f"{CAMARA_BASE}/deputados/{deputado_id}/proposicoes"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("dados", [])
    except requests.RequestException as e:
        print(f"[Câmara] Erro ao buscar proposições do deputado {deputado_id}: {e}")
        return []


def obter_historico_legislativo(nome_candidato: str):
    """
    Busca histórico legislativo completo de um candidato que seja/tenha sido deputado.
    Retorna dados formatados ou None se não encontrado.
    """
    deputados = buscar_deputados_por_nome(nome_candidato)
    if not deputados:
        return None

    deputado = deputados[0]
    dep_id = deputado["id"]
    proposicoes = buscar_proposicoes_deputado(dep_id)

    return {
        "presenca_percent": None,  # calcular a partir de endpoint de frequência
        "projetos_propostos": len(proposicoes),
        "votos_em_pautas_politicas": 0,  # calcular a partir de endpoint de votações
        "fonte": f"https://dadosabertos.camara.leg.br/api/v2/deputados/{dep_id}",
    }
