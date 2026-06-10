"""
Coletor Portal da Transparência
API: https://api.portaldatransparencia.gov.br/

Endpoints:
- /api-de-dados/contratos — contratos por órgão
- /api-de-dados/orgaos-siafi — lista de órgãos

Autenticação: header HTTP chave-api-dados
"""
import os
import requests
from typing import Optional

PORTAL_BASE = "https://api.portaldatransparencia.gov.br/api-de-dados"
PORTAL_TOKEN = os.environ.get("PORTAL_TRANSPARENCIA_TOKEN", "")

HEADERS = {
    "User-Agent": "CandidatAI/1.0 (painel-transparencia)",
    "Accept": "application/json",
    "chave-api-dados": PORTAL_TOKEN,
}

ORGAOS_INTERESSE = [
    {"codigo": "25000", "nome": "Ministério da Fazenda"},
    {"codigo": "01000", "nome": "Câmara dos Deputados"},
    {"codigo": "02000", "nome": "Senado Federal"},
    {"codigo": "20000", "nome": "Presidência da República"},
    {"codigo": "30000", "nome": "Ministério da Justiça"},
    {"codigo": "36000", "nome": "Ministério da Saúde"},
    {"codigo": "26000", "nome": "Ministério da Educação"},
]


def buscar_contratos_por_orgao(codigo_orgao: str, pagina: int = 1):
    """Busca contratos de um órgão específico."""
    url = f"{PORTAL_BASE}/contratos"
    params = {"codigoOrgao": codigo_orgao, "pagina": pagina}

    try:
        resp = requests.get(url, params=params, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"[Portal] Erro ao buscar contratos do órgão {codigo_orgao}: {e}")
        return []


def buscar_contratos_por_empresa(cnpj_empresa: str, codigo_orgao: Optional[str] = None):
    """
    Busca contratos onde uma empresa específica (CNPJ) é contratada.
    Itera por órgãos de interesse ou usa um órgão específico.
    """
    resultados = []
    orgaos = [{"codigo": codigo_orgao}] if codigo_orgao else ORGAOS_INTERESSE

    for orgao in orgaos:
        pagina = 1
        while pagina <= 3:  # limite de 3 páginas por órgão
            contratos = buscar_contratos_por_orgao(orgao["codigo"], pagina)
            if not contratos:
                break

            for c in contratos:
                # Verificar se o CNPJ da empresa contratada aparece no contrato
                # Nota: a API não tem filtro direto por CNPJ — fazemos no lado do cliente
                compra = c.get("compra", {})
                org_data = c.get("unidadeGestora", {}).get("orgaoVinculado", {})
                if org_data.get("cnpj") == cnpj_empresa:
                    resultados.append({
                        "empresa": c.get("unidadeGestora", {}).get("nome", ""),
                        "contrato_numero": c.get("numero", ""),
                        "valor": 0,  # API não expõe valor diretamente nesse endpoint
                        "orgao_contratante": c.get("unidadeGestora", {}).get("orgaoVinculado", {}).get("nome", ""),
                        "data_assinatura": "",  # API não expõe data nesse endpoint
                        "fonte": f"https://portaldatransparencia.gov.br/contratos/{c.get('id', '')}",
                    })

            pagina += 1

    return resultados


def obter_orgaos_disponiveis():
    """Lista todos os órgãos SIAFI disponíveis na API."""
    url = f"{PORTAL_BASE}/orgaos-siafi"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"[Portal] Erro ao listar órgãos: {e}")
        return []
