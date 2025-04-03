import sqlite3
from datetime import datetime

# Conectar ao banco de dados 'cliente.db' e criar um cursor para executar comandos SQL
conn = sqlite3.connect('cliente.db')
cursor = conn.cursor()

# Criar a tabela 'mercadoria' se ela não existir
cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS mercadoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cpf VARCHAR(14) NOT NULL,
        nome VARCHAR(50) NOT NULL,
        data_nascimento DATE NOT NULL,
        data_compra DATE NOT NULL,
        serie TEXT NOT NULL,
        tipo VARCHAR(30) NOT NULL,
        marca VARCHAR(30) NOT NULL,
        modelo VARCHAR(30) NOT NULL,
        quantidade INTEGER NOT NULL,
        valor_unitario REAL NOT NULL,
        valor_total REAL NOT NULL
    )
''')
conn.commit()


# Função: cadastrar_produto
# Descrição: Cadastra um novo produto na tabela 'mercadoria'. Verifica se todos os campos obrigatórios
# estão preenchidos, se os valores informados (quantidade e valor_unitário) são positivos e realiza
# o cálculo do valor_total antes de inserir no banco de dados.
def cadastrar_produto(cpf, nome, serie, tipo, marca, modelo, quantidade, valor_unitario, data_compra=None, data_nascimento=None):
    if not all([cpf, nome, data_nascimento, serie, tipo, marca, modelo, quantidade, valor_unitario]):
        print("Erro: Todos os campos são obrigatórios.")
        return "Erro: Dados obrigatórios não preenchidos."

    if quantidade <= 0 or valor_unitario <= 0:
        print("Erro: A quantidade e o valor unitário devem ser positivos.")
        return "Erro: Quantidade ou valor unitário inválido."

    # Se data_compra não for informada, utiliza a data/hora atual no formato DD-MM-YYYY HH:MM:SS
    if not data_compra:
        data_compra = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Calcula o valor total da compra
    valor_total = valor_unitario * quantidade

    try:
        cursor.execute(''' 
            INSERT INTO mercadoria (cpf, nome, data_nascimento, data_compra, serie, tipo, marca, modelo, quantidade, valor_unitario, valor_total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (cpf, nome, data_nascimento, data_compra, serie, tipo, marca, modelo, quantidade, valor_unitario, valor_total))
        conn.commit()
        print("Produto cadastrado com sucesso!")
        return "Produto cadastrado com sucesso!"
    except sqlite3.IntegrityError:
        print(f"Erro: Produto com CPF {cpf} já existe.")
        return f"Erro: Produto com CPF {cpf} já existe."
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return f"Erro inesperado: {e}"


# Função: listar_produtos_cliente
# Descrição: Consulta e imprime todos os registros da tabela 'mercadoria'. Caso nenhum produto seja encontrado,
# informa que nenhum produto foi encontrado.
def listar_produtos_cliente():
    cursor.execute("SELECT * FROM mercadoria")
    produtos = cursor.fetchall()
    if produtos:
        for produto in produtos:
            print(produto)
    else:
        print("Nenhum produto encontrado.")


# Função: buscar_produto
# Descrição: Busca um produto específico na tabela 'mercadoria' com base no CPF informado.
# Caso o produto seja encontrado, ele é impresso e retornado; caso contrário, é exibida uma mensagem de erro.
def buscar_produto(cpf):
    cursor.execute("SELECT * FROM mercadoria WHERE cpf = ?", (cpf,))
    produto = cursor.fetchone()
    if produto:
        print(produto)
        return produto
    else:
        print("Produto não encontrado.")
        return "Produto não encontrado."


# Função: atualizar_produto
# Descrição: Atualiza os dados de um produto existente na tabela 'mercadoria' com base no CPF.
# Apenas os campos informados serão atualizados; os demais permanecem com os valores atuais.
def atualizar_produto(cpf, nome=None, data_nascimento=None, serie=None, tipo=None, marca=None, modelo=None, quantidade=None, valor_unitario=None, data_compra=None):
    cursor.execute("SELECT * FROM mercadoria WHERE cpf = ?", (cpf,))
    produto = cursor.fetchone()
    if not produto:
        print("Produto não encontrado.")
        return "Produto não encontrado."

    # Se algum valor não for informado, mantém o valor que já está no registro
    nome = nome if nome is not None else produto[2]
    data_nascimento = data_nascimento if data_nascimento is not None else produto[3]
    data_compra = data_compra if data_compra is not None else produto[4]
    serie = serie if serie is not None else produto[5]
    tipo = tipo if tipo is not None else produto[6]
    marca = marca if marca is not None else produto[7]
    modelo = modelo if modelo is not None else produto[8]
    quantidade = quantidade if quantidade is not None else produto[9]
    valor_unitario = valor_unitario if valor_unitario is not None else produto[10]

    # Recalcula o valor total com base na quantidade e valor unitário
    valor_total = valor_unitario * quantidade

    cursor.execute(''' 
        UPDATE mercadoria
        SET nome = ?, data_nascimento = ?, data_compra = ?, serie = ?, tipo = ?, marca = ?, modelo = ?, quantidade = ?, valor_unitario = ?, valor_total = ?
        WHERE cpf = ?
    ''', (nome, data_nascimento, data_compra, serie, tipo, marca, modelo, quantidade, valor_unitario, valor_total, cpf))

    conn.commit()
    print("Produto atualizado com sucesso!")
    return "Produto atualizado com sucesso!"


# Função: deletar_produto
# Descrição: Exclui um produto da tabela 'mercadoria' com base no CPF informado.
# Verifica se o produto existe antes de tentar a exclusão.
def deletar_produto(cpf):
    cursor.execute("SELECT * FROM mercadoria WHERE cpf = ?", (cpf,))
    if not cursor.fetchone():
        print("Produto não encontrado.")
        return "Produto não encontrado."

    cursor.execute("DELETE FROM mercadoria WHERE cpf = ?", (cpf,))
    conn.commit()
    print("Produto excluído com sucesso!")
    return "Produto excluído com sucesso!"
