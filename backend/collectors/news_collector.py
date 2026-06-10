"""
Coletor de Notícias (GNews API)
API: https://gnews.io/api/v4/

Busca matérias recentes sobre candidatos nos últimos 12 meses.
Requer API key: GNEWS_API_KEY no ambiente.
"""
import os
import requests

GNEWS_API_KEY = os.environ.get("GNEWS_API_KEY", "")
GNEWS_BASE = "https://gnews.io/api/v4"


def buscar_materias_candidato(nome: str, max_results: int = 10):
    """
    Busca matérias de notícias mencionando o candidato na GNews API.
    Retorna lista de matérias ou None se API key não configurada.
    """
    if not GNEWS_API_KEY:
        print(f"[GNews] API key não configurada. Pulando busca para '{nome}'.")
        return None

    url = f"{GNEWS_BASE}/search"
    params = {
        "q": nome,
        "lang": "pt",
        "country": "br",
        "max": max_results,
        "sortby": "publishedAt",
        "token": GNEWS_API_KEY,
    }

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        articles = data.get("articles", [])
        return [
            {
                "titulo": a.get("title", ""),
                "veiculo": a.get("source", {}).get("name", ""),
                "data": a.get("publishedAt", "")[:10],
                "url": a.get("url", ""),
                "fonte_api": "GNews API",
            }
            for a in articles
        ]
    except requests.RequestException as e:
        print(f"[GNews] Erro ao buscar matérias para '{nome}': {e}")
        return []


def buscar_materias_candidato_fallback(nome: str, max_results: int = 10):
    """
    Fallback: busca via NewsAPI se GNews não disponível.
    """
    newsapi_key = os.environ.get("NEWSAPI_KEY", "")
    if not newsapi_key:
        return None

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": nome,
        "language": "pt",
        "sortBy": "publishedAt",
        "pageSize": max_results,
        "apiKey": newsapi_key,
    }
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        articles = data.get("articles", [])
        return [
            {
                "titulo": a.get("title", ""),
                "veiculo": a.get("source", {}).get("name", ""),
                "data": (a.get("publishedAt", "") or "")[:10],
                "url": a.get("url", ""),
                "fonte_api": "NewsAPI",
            }
            for a in articles
        ]
    except requests.RequestException as e:
        print(f"[NewsAPI] Erro: {e}")
        return []
