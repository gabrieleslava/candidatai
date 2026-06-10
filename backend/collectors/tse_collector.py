"""
Coletor TSE — DivulgaCand + Prestação de Contas
API: https://dadosabertos.tse.jus.br/

Endpoints usados:
- /api/v2/eleicoes/2026/candidatos — lista de candidatos
- /api/v2/eleicoes/2026/bens/{candidato_id} — bens declarados
- /api/v2/eleicoes/2026/prestacao-contas/{candidato_id} — gastos e doadores
"""
import requests
import unicodedata
from typing import Optional

TSE_BASE = "https://dadosabertos.tse.jus.br/api/v2"

HEADERS = {
    "User-Agent": "CandidatAI/1.0 (painel-transparencia; contato@exemplo.com)",
    "Accept": "application/json",
}


def normalize_nome(nome: str) -> str:
    """Remove acentos, lowercase, strip."""
    n = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
    return n.lower().strip()


def buscar_candidatos_2026(cargo: Optional[str] = None, estado: Optional[str] = None):
    """
    Busca candidatos das eleições 2026 no DivulgaCand.
    Nota: a API real pode ter endpoints diferentes dependendo da versão.
    Esta função implementa a interface esperada.
    """
    # TSE organiza por eleição e cargo. Exemplo:
    # /api/v2/eleicoes/2026/candidatos?cargo=presidente&uf=SP
    url = f"{TSE_BASE}/eleicoes/2026/candidatos"
    params = {}
    if cargo:
        params["cargo"] = cargo
    if estado and estado != "Nacional":
        params["uf"] = estado

    try:
        resp = requests.get(url, params=params, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("dados", data.get("data", []))
    except requests.RequestException as e:
        print(f"[TSE] Erro ao buscar candidatos: {e}")
        return []


def buscar_bens_candidato(candidato_id: str):
    """Busca bens declarados de um candidato no DivulgaCand."""
    url = f"{TSE_BASE}/eleicoes/2026/bens/{candidato_id}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("dados", data.get("data", []))
    except requests.RequestException as e:
        print(f"[TSE] Erro ao buscar bens de {candidato_id}: {e}")
        return []


def buscar_prestacao_contas(candidato_id: str):
    """Busca prestação de contas (gastos + doadores) de um candidato."""
    url = f"{TSE_BASE}/eleicoes/2026/prestacao-contas/{candidato_id}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return {
            "total_declarado": data.get("totalDespesas", data.get("total", 0)),
            "doadores": data.get("doadores", data.get("doador", [])),
            "fonte": url,
        }
    except requests.RequestException as e:
        print(f"[TSE] Erro ao buscar contas de {candidato_id}: {e}")
        return {"total_declarado": 0, "doadores": [], "fonte": url}
