import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "candidatai.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS candidatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            nome_normalizado TEXT NOT NULL UNIQUE,
            numero INTEGER,
            partido TEXT NOT NULL,
            cargo TEXT NOT NULL,
            estado TEXT NOT NULL,
            foto_url TEXT,
            intencao_voto REAL,
            pesquisa_fonte TEXT,
            indicadores TEXT NOT NULL DEFAULT '{}',
            data_atualizacao TEXT NOT NULL DEFAULT (date('now'))
        );

        CREATE TABLE IF NOT EXISTS secao_processos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidato_id INTEGER NOT NULL REFERENCES candidatos(id) ON DELETE CASCADE,
            tipo TEXT NOT NULL,
            instancia TEXT NOT NULL,
            status TEXT NOT NULL,
            data_inicio TEXT,
            data_decisao TEXT,
            fonte TEXT NOT NULL,
            observacao TEXT
        );

        CREATE TABLE IF NOT EXISTS secao_materias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidato_id INTEGER NOT NULL REFERENCES candidatos(id) ON DELETE CASCADE,
            titulo TEXT NOT NULL,
            veiculo TEXT NOT NULL,
            data TEXT NOT NULL,
            url TEXT NOT NULL,
            fonte_api TEXT
        );

        CREATE TABLE IF NOT EXISTS secao_gastos_campanha (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidato_id INTEGER NOT NULL UNIQUE REFERENCES candidatos(id) ON DELETE CASCADE,
            total_declarado INTEGER NOT NULL DEFAULT 0,
            fonte TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS secao_doadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gasto_id INTEGER NOT NULL REFERENCES secao_gastos_campanha(id) ON DELETE CASCADE,
            nome TEXT NOT NULL,
            valor INTEGER NOT NULL,
            cpf_cnpj TEXT,
            fonte TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS secao_bens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidato_id INTEGER NOT NULL REFERENCES candidatos(id) ON DELETE CASCADE,
            descricao TEXT NOT NULL,
            valor INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            fonte TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS secao_historico_legislativo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidato_id INTEGER NOT NULL UNIQUE REFERENCES candidatos(id) ON DELETE CASCADE,
            presenca_percent INTEGER,
            projetos_propostos INTEGER NOT NULL DEFAULT 0,
            votos_em_pautas_politicas INTEGER NOT NULL DEFAULT 0,
            fonte TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS secao_contratos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidato_id INTEGER NOT NULL REFERENCES candidatos(id) ON DELETE CASCADE,
            empresa TEXT NOT NULL,
            contrato_numero TEXT NOT NULL,
            valor INTEGER NOT NULL,
            orgao_contratante TEXT NOT NULL,
            data_assinatura TEXT NOT NULL,
            fonte TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_candidatos_cargo ON candidatos(cargo);
        CREATE INDEX IF NOT EXISTS idx_candidatos_estado ON candidatos(estado);
        CREATE INDEX IF NOT EXISTS idx_candidatos_intencao ON candidatos(intencao_voto DESC);
        CREATE INDEX IF NOT EXISTS idx_processos_candidato ON secao_processos(candidato_id);
        CREATE INDEX IF NOT EXISTS idx_materias_candidato ON secao_materias(candidato_id);
    """)
    conn.commit()
    conn.close()
