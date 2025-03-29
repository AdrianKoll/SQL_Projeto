import sqlite3

# Conectar ao banco de dados (cria um arquivo se não existir)
conexao = sqlite3.connect('estoque.db')

# Criar um cursor para executar comandos SQL
cursor = conexao.cursor()

# Criar a tabela 'mercadoria'
cursor.execute('''
CREATE TABLE IF NOT EXISTS mercadoria (
    cpf TEXT PRIMARY KEY NOT NULL,
    nome VARCHAR(35) NOT NULL,
    data_nascimento TEXT NOT NULL,
    categoria VARCHAR(30) NOT NULL,
    quantidade INTEGER NOT NULL,
    preco REAL NOT NULL,
    data_compra TEXT DEFAULT (datetime('now', 'localtime')) NOT NULL
);
''')

print("Tabela criada com sucesso!")

# Confirmar as mudanças e fechar a conexão
conexao.commit()
conexao.close()