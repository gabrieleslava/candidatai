"""
Coletor DataJud (CNJ) — Processos Judiciais
API GraphQL: https://datajud.cnj.jus.br/

Permite consultar processos por nome da parte (candidato).
É uma API GraphQL — usamos requests com query GraphQL.
"""
import requests
import unicodedata
from typing import Optional

DATAJUD_URL = "https://datajud.cnj.jus.br/graphql"

HEADERS = {
    "User-Agent": "CandidatAI/1.0 (painel-transparencia; contato@exemplo.com)",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

QUERY_PROCESSOS = """
query buscarProcessos($nome: String!, $limit: Int!) {
  processos(where: { parte: { nome: { _ilike: $nome } } }, limit: $limit) {
    id
    numero
    tipo
    instancia
    status
    dataInicio
    dataDecisao
    observacao
    tribunal
  }
}
"""


def buscar_processos_por_nome(nome: str, limit: int = 20):
    """Busca processos judiciais associados a um nome de parte no DataJud."""
    nome_normalizado = f"%{nome}%"  # busca parcial case-insensitive

    query = """
    query BuscarProcessos($nome: String, $limit: Int) {
      processos(first: $limit, where: {partes: {nome: {_ilike: $nome}}}) {
        nodes {
          id
          numero
          tipo
          instancia
          status
          dataInicio
          dataDecisao
          tribunal
          observacao
        }
      }
    }
    """

    payload = {
        "query": query,
        "variables": {"nome": nome_normalizado, "limit": limit},
    }

    try:
        resp = requests.post(DATAJUD_URL, json=payload, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        processos = data.get("data", {}).get("processos", {}).get("nodes", [])
        return processos
    except requests.RequestException as e:
        print(f"[DataJud] Erro ao buscar processos de '{nome}': {e}")
        return []


def mapear_processo_para_modelo(proc: dict) -> dict:
    """Converte processo do DataJud para o formato interno do CandidatAI."""
    return {
        "tipo": proc.get("tipo", "Não especificado"),
        "instancia": proc.get("tribunal", proc.get("instancia", "Não informada")),
        "status": proc.get("status", "em_andamento"),
        "data_inicio": proc.get("dataInicio"),
        "data_decisao": proc.get("dataDecisao"),
        "fonte": f"https://datajud.cnj.jus.br/processo/{proc.get('numero', proc.get('id', ''))}",
        "observacao": proc.get("observacao"),
    }
