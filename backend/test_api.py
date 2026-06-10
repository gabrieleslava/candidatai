"""
Testes unitários para a API CandidatAI.
Usa pytest + FastAPI TestClient com banco temporário em memória.
"""
import json
import pytest
from fastapi.testclient import TestClient

# Força o banco a usar um arquivo temporário para isolar dos dados de dev
import os
import tempfile

os.environ["GNEWS_API_KEY"] = "test-key"
os.environ["PORTAL_TRANSPARENCIA_TOKEN"] = "test-token"
os.environ["CANDIDATAI_TEST"] = "1"


@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch):
    """Cria um banco temporário para cada teste, isolando dos dados de dev."""
    import database

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    tmp_path = tmp.name
    tmp.close()

    monkeypatch.setattr(database, "DB_PATH", tmp_path)
    database.init_db()

    # Seed apenas com 2 candidatos para testes rápidos
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO candidatos (nome, nome_normalizado, numero, partido, cargo, estado, foto_url,
           intencao_voto, pesquisa_fonte, indicadores)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            "Maria Souza", "maria souza", 13, "PT", "Presidência", "Nacional",
            "", 23.0, "Datafolha — 05/06/2026",
            json.dumps({
                "processos_totais": 3, "processos_condenacao_transitada": 0,
                "processos_em_andamento": 3, "materias_12m": 12,
                "doacoes_empresas_investigadas": 1, "patrimonio_declarado": 1450000,
                "presenca_legislativa_percent": None,
            }),
        ),
    )
    cursor.execute(
        """INSERT INTO candidatos (nome, nome_normalizado, numero, partido, cargo, estado, foto_url,
           intencao_voto, pesquisa_fonte, indicadores)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            "Carlos Lima", "carlos lima", 22, "PL", "Presidência", "Nacional",
            "", 18.0, "Datafolha — 05/06/2026",
            json.dumps({
                "processos_totais": 7, "processos_condenacao_transitada": 1,
                "processos_em_andamento": 5, "materias_12m": 28,
                "doacoes_empresas_investigadas": 3, "patrimonio_declarado": 5200000,
                "presenca_legislativa_percent": 78,
            }),
        ),
    )
    conn.commit()

    # Adiciona processos para o candidato 2
    cursor.execute(
        """INSERT INTO secao_processos (candidato_id, tipo, instancia, status, data_inicio, data_decisao, fonte, observacao)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (2, "Corrupção passiva", "STJ", "transitada_em_julgado", "2020-05-10", "2024-08-12",
         "https://datajud.cnj.jus.br/processo/0004", "Condenação"),
    )
    conn.commit()
    conn.close()

    yield

    try:
        os.unlink(tmp_path)
    except OSError:
        pass


@pytest.fixture
def client(setup_test_db):
    from main import app
    with TestClient(app) as c:
        yield c


class TestStatus:
    def test_status_retorna_integracoes(self, client):
        resp = client.get("/api/status")
        assert resp.status_code == 200
        data = resp.json()
        assert "integracoes" in data
        assert "modo" in data
        assert data["modo"] == "hibrido"
        assert "camara" in data["integracoes"]


class TestFiltros:
    def test_filtros_retorna_cargos_e_estados(self, client):
        resp = client.get("/api/filtros")
        assert resp.status_code == 200
        data = resp.json()
        assert "cargos" in data
        assert "estados" in data
        assert "Presidência" in data["cargos"]
        assert "Nacional" in data["estados"]


class TestListarCandidatos:
    def test_lista_todos(self, client):
        resp = client.get("/api/candidatos")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2

    def test_filtra_por_cargo(self, client):
        resp = client.get("/api/candidatos?cargo=Presidência")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2
        for c in data:
            assert c["cargo"] == "Presidência"

    def test_filtra_por_cargo_inexistente(self, client):
        resp = client.get("/api/candidatos?cargo=Vereador")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 0

    def test_filtra_por_busca(self, client):
        resp = client.get("/api/candidatos?busca=Maria")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["nome"] == "Maria Souza"

    def test_filtra_por_busca_case_insensitive(self, client):
        resp = client.get("/api/candidatos?busca=maria")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1

    def test_filtra_tem_processos(self, client):
        resp = client.get("/api/candidatos?tem_processos=true")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 1
        for c in data:
            assert c["indicadores"]["processos_totais"] > 0

    def test_filtra_tem_condenacao(self, client):
        resp = client.get("/api/candidatos?tem_condenacao=true")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 1
        for c in data:
            assert c["indicadores"]["processos_condenacao_transitada"] > 0


class TestPerfilCandidato:
    def test_perfil_existente(self, client):
        resp = client.get("/api/candidatos/1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["candidato"]["nome"] == "Maria Souza"
        assert data["candidato"]["partido"] == "PT"
        assert "secoes" in data
        assert "versao_schema" in data

    def test_perfil_inexistente_404(self, client):
        resp = client.get("/api/candidatos/999")
        assert resp.status_code == 404

    def test_perfil_com_processos(self, client):
        resp = client.get("/api/candidatos/2")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["secoes"]["processos"]) >= 1


class TestCompararCandidatos:
    def test_comparar_dois_candidatos(self, client):
        resp = client.get("/api/candidatos/comparar?ids=1,2")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2
        assert data[0]["candidato"]["nome"] == "Maria Souza"
        assert data[1]["candidato"]["nome"] == "Carlos Lima"

    def test_comparar_menos_de_2_ids(self, client):
        resp = client.get("/api/candidatos/comparar?ids=1")
        assert resp.status_code == 400

    def test_comparar_mais_de_4_ids(self, client):
        resp = client.get("/api/candidatos/comparar?ids=1,2,3,4,5")
        assert resp.status_code == 400

    def test_comparar_ids_inexistentes_sao_ignorados(self, client):
        resp = client.get("/api/candidatos/comparar?ids=1,999")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
