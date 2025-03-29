import sqlite3
from datetime import datetime

# Conectar ao banco de dados
def conectar():
    return sqlite3.connect('cliente.db')

# Função para criar a tabela (se não existir)
def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS mercadoria (
            cpf TEXT PRIMARY KEY NOT NULL,
            nome TEXT NOT NULL,
            data_nascimento TEXT NOT NULL,
            data_compra TEXT NOT NULL,
            categoria TEXT NOT NULL,
            serie TEXT NOT NULL,
            tipo TEXT NOT NULL,
            marca TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            valor_unitario REAL NOT NULL,
            valor_total REAL NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

# Função para cadastrar um produto
def cadastrar_produto(cpf, nome, categoria, serie, tipo, marca, quantidade, valor_unitario, data_compra=None, data_nascimento=None):
    # Verificar se todos os campos obrigatórios foram preenchidos
    if not cpf or not nome or not categoria or quantidade is None or valor_unitario is None or not data_nascimento or not serie or not tipo or not marca:
        print("Erro: Todos os campos (CPF, Nome, Data de Nascimento, Categoria, Quantidade, Valor Unitário, Série, Tipo, Marca) são obrigatórios.")
        return "Erro: Dados obrigatórios não preenchidos."

    # Verificar se a quantidade e o valor unitário são válidos
    if quantidade <= 0 or valor_unitario <= 0:
        print("Erro: A quantidade e o valor unitário devem ser positivos.")
        return "Erro: Quantidade ou valor unitário inválido."

    conexao = conectar()
    cursor = conexao.cursor()

    # Se não fornecer a data de compra, usa a data atual
    if not data_compra:
        data_compra = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Calcular o valor total da compra
    valor_total = valor_unitario * quantidade  # Valor total da compra

    try:
        cursor.execute(''' 
            INSERT INTO mercadoria (cpf, nome, data_nascimento, data_compra, categoria, serie, tipo, marca, quantidade, valor_unitario, valor_total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (cpf, nome, data_nascimento, data_compra, categoria, serie, tipo, marca, quantidade, valor_unitario, valor_total))
        conexao.commit()
        print("Produto cadastrado com sucesso!")
        return "Produto cadastrado com sucesso!"
    except sqlite3.IntegrityError:
        print(f"Erro: Produto com CPF {cpf} já existe.")
        return f"Erro: Produto com CPF {cpf} já existe."
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return f"Erro inesperado: {e}"
    finally:
        conexao.close()

# Função para listar todos os produtos
def listar_produtos_cliente():
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
        return produto
    else:
        print("Produto não encontrado.")
        return "Produto não encontrado."

# Função para atualizar um produto pelo CPF
def atualizar_produto(cpf, nome=None, data_nascimento=None, categoria=None, serie=None, tipo=None, marca=None, quantidade=None, valor_unitario=None, data_compra=None):
    conexao = conectar()
    cursor = conexao.cursor()

    # Verificar se o produto existe
    cursor.execute("SELECT * FROM mercadoria WHERE cpf = ?", (cpf,))
    produto = cursor.fetchone()

    if not produto:
        print("Produto não encontrado.")
        conexao.close()
        return "Produto não encontrado."

    # Manter valores antigos se não forem fornecidos
    nome = nome if nome else produto[1]
    data_nascimento = data_nascimento if data_nascimento else produto[2]
    data_compra = data_compra if data_compra else produto[3]
    categoria = categoria if categoria else produto[4]
    serie = serie if serie else produto[5]
    tipo = tipo if tipo else produto[6]
    marca = marca if marca else produto[7]
    quantidade = quantidade if quantidade else produto[8]
    valor_unitario = valor_unitario if valor_unitario else produto[9]

    # Calcular o valor total (se a quantidade ou valor_unitario forem atualizados)
    valor_total = valor_unitario * quantidade

    # Atualizar produto
    cursor.execute(''' 
        UPDATE mercadoria
        SET nome = ?, data_nascimento = ?, data_compra = ?, categoria = ?, serie = ?, tipo = ?, marca = ?, quantidade = ?, valor_unitario = ?, valor_total = ?
        WHERE cpf = ?
    ''', (nome, data_nascimento, data_compra, categoria, serie, tipo, marca, quantidade, valor_unitario, valor_total, cpf))

    conexao.commit()
    print("Produto atualizado com sucesso!")
    conexao.close()
    return "Produto atualizado com sucesso!"

# Função para deletar um produto pelo CPF
def deletar_produto(cpf):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM mercadoria WHERE cpf = ?", (cpf,))
    if not cursor.fetchone():
        print("Produto não encontrado.")
        conexao.close()
        return "Produto não encontrado."

    cursor.execute("DELETE FROM mercadoria WHERE cpf = ?", (cpf,))
    conexao.commit()
    print("Produto excluído com sucesso!")
    conexao.close()
    return "Produto excluído com sucesso!"

# Criação da tabela ao iniciar o script (caso ainda não exista)
criar_tabela()
