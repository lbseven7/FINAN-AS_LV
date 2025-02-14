import sqlite3

def conectar_banco():
    return sqlite3.connect("orcamento.db")

def criar_tabelas(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS receitas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        origem TEXT NOT NULL,
        valor REAL NOT NULL,
        data TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS despesas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        categoria TEXT NOT NULL,
        valor REAL NOT NULL,
        responsavel TEXT NOT NULL,
        data TEXT NOT NULL
    )
    """)
    conn.commit()

def atualizar_valores(conn):
    cursor = conn.cursor()
    cursor.execute("UPDATE despesas SET responsavel = 'Esposo' WHERE responsavel = 'Leo'")
    cursor.execute("UPDATE despesas SET responsavel = 'Esposa' WHERE responsavel = 'Vivian'")
    conn.commit()

def atualizar_meses_vazios(conn):
    conn.execute("""
        UPDATE receitas
        SET mes = strftime('%m', data)
        WHERE mes IS NULL
    """)
    
    conn.execute("""
        UPDATE despesas
        SET mes = strftime('%m', data)
        WHERE mes IS NULL
    """)
    
    conn.commit()
