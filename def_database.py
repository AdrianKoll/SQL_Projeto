import sqlite3
from datetime import datetime

# Conectar ao banco de dados
def conectar():
    return sqlite3.connect('estoque.db')

# Função para criar a tabela (se não existir)
def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mercadoria (
            cpf TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            data_nascimento TEXT NOT NULL,
            data_compra TEXT,
            categoria TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

# Função para cadastrar um produto
def cadastrar_produto(cpf, nome, categoria, quantidade, preco, data_compra=None, data_nascimento=None):
    # Verificar se todos os campos obrigatórios foram preenchidos
    if not cpf or not nome or not categoria or quantidade is None or preco is None or not data_nascimento:
        print("Erro: Todos os campos (CPF, Nome, Data de Nascimento, Categoria, Quantidade e Preço) são obrigatórios.")
        return

    conexao = conectar()
    cursor = conexao.cursor()

    # Se não fornecer a data de compra, usa a data atual
    if not data_compra:
        data_compra = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cursor.execute('''
            INSERT INTO mercadoria (cpf, nome, data_nascimento, data_compra, categoria, quantidade, preco)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (cpf, nome, data_nascimento, data_compra, categoria, quantidade, preco))
        conexao.commit()
        print("Produto cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print(f"Erro: Produto com CPF {cpf} já existe.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        conexao.close()

# Função para listar todos os produtos
def listar_produtos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM mercadoria")
    produtos = cursor.fetchall()
    conexao.close()

    if produtos:
        for produto in produtos:
            print(produto)
    else:
        print("Nenhum produto encontrado.")

# Função para buscar um produto pelo CPF
def buscar_produto(cpf):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM mercadoria WHERE cpf = ?", (cpf,))
    produto = cursor.fetchone()
    conexao.close()

    if produto:
        print(produto)
    else:
        print("Produto não encontrado.")

# Função para atualizar um produto pelo CPF
def atualizar_produto(cpf, nome=None,data_nascimento=None, categoria=None, quantidade=None, preco=None, data_compra=None):
    conexao = conectar()
    cursor = conexao.cursor()

    # Verificar se o produto existe
    cursor.execute("SELECT * FROM mercadoria WHERE cpf = ?", (cpf,))
    produto = cursor.fetchone()

    if not produto:
        print("Produto não encontrado.")
        conexao.close()
        return

    # Manter valores antigos se não forem fornecidos
    nome = nome if nome else produto[1]
    data_nascimento = data_nascimento if data_nascimento else produto[2]
    data_compra = data_compra if data_compra else produto[3]
    categoria = categoria if categoria else produto[4]
    quantidade = quantidade if quantidade else produto[5]
    preco = preco if preco else produto[6]

    # Atualizar produto
    cursor.execute('''
        UPDATE mercadoria
        SET nome = ?, data_nascimento = ?, data_compra = ?, categoria = ?, quantidade = ?, preco = ?
        WHERE cpf = ?
    ''', (nome, data_nascimento, data_compra, categoria, quantidade, preco, cpf))

    conexao.commit()
    print("Produto atualizado com sucesso!")
    conexao.close()

# Função para deletar um produto pelo CPF
def deletar_produto(cpf):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM mercadoria WHERE cpf = ?", (cpf,))
    if not cursor.fetchone():
        print("Produto não encontrado.")
        conexao.close()
        return

    cursor.execute("DELETE FROM mercadoria WHERE cpf = ?", (cpf,))
    conexao.commit()
    print("Produto excluído com sucesso!")
    conexao.close()

# Criação da tabela ao iniciar o script (caso ainda não exista)
criar_tabela()
