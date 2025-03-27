import sqlite3

# Cria (ou liga-se a) uma base de dados local chamada contactos.db
conn = sqlite3.connect("contactos.db")

# Cria um cursor para executar comandos SQL
cursor = conn.cursor()

# Cria a tabela
cursor.execute("""
CREATE TABLE IF NOT EXISTS contactos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    autocarros TEXT
);
""")

# Guarda alterações e fecha ligação
conn.commit()
conn.close()

print("Base de dados e tabela criadas com sucesso.")
