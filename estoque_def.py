import sqlite3
from datetime import datetime

# Conectando ao banco de dados 'estoque.db' e criando o cursor
conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

# ---------------------------------------------------------------------------
# Função: criar_tabela()
# Descrição: Cria a tabela de estoque, se ela ainda não existir, com os campos:
#           série (chave primária), tipo, marca, modelo, quantidade, preço, e data/hora.
# ---------------------------------------------------------------------------
def criar_tabela():
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS estoque ( 
        serie VARCHAR(40) PRIMARY KEY, 
        tipo VARCHAR(35) NOT NULL, 
        marca VARCHAR(35) NOT NULL,
        modelo VARCHAR(35) NOT NULL,
        quantidade INTEGER NOT NULL, 
        preco REAL NOT NULL, 
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP 
    ) 
    ''')
    conn.commit()

# Chamar a função para garantir que a tabela exista
criar_tabela()

# ---------------------------------------------------------------------------
# Função: produto_existe(serie)
# Descrição: Verifica se já existe um produto no estoque com a série informada.
# Retorna True se existir, caso contrário False.
# ---------------------------------------------------------------------------
def produto_existe(serie):
    cursor.execute('SELECT 1 FROM estoque WHERE serie = ?', (serie,))
    return cursor.fetchone() is not None

# ---------------------------------------------------------------------------
# Função: adicionar_produto(serie, tipo, marca, modelo, quantidade, preco)
# Descrição: Adiciona um novo produto ao estoque, após realizar as validações:
#           - Verifica se o produto já existe (pela série).
#           - Verifica se quantidade e preço são maiores que zero.
#           - Insere o produto com a data/hora atual.
# ---------------------------------------------------------------------------
def adicionar_produto(serie, tipo, marca, modelo, quantidade, preco):
    if produto_existe(serie):
        print("Erro: Produto com essa série já existe!")
        return

    if quantidade <= 0 or preco <= 0:
        print("Erro: Quantidade e preço devem ser maiores que zero!")
        return

    data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(''' 
    INSERT INTO estoque (serie, tipo, marca, modelo, quantidade, preco, data_hora) 
    VALUES (?, ?, ?, ?, ?, ?, ?) 
    ''', (serie, tipo, marca, modelo, quantidade, preco, data_hora))
    conn.commit()
    print("Produto adicionado com sucesso!")

# ---------------------------------------------------------------------------
# Função: listar_produtos()
# Descrição: Recupera e imprime todos os produtos cadastrados na tabela 'estoque'.
# Retorna uma lista de todos os produtos encontrados.
# ---------------------------------------------------------------------------
def listar_produtos():
    cursor.execute('SELECT * FROM estoque')
    produtos = cursor.fetchall()
    for produto in produtos:
        print(produto)
    return produtos

# ---------------------------------------------------------------------------
# Função: atualizar_produto(serie, tipo, marca, modelo, quantidade, preco)
# Descrição: Atualiza os dados de um produto específico no estoque.
#           Apenas atualiza os campos que forem informados; os demais permanecem inalterados.
# ---------------------------------------------------------------------------
def atualizar_produto(serie, tipo=None, marca=None, modelo=None, quantidade=None, preco=None):
    if not produto_existe(serie):
        print("Erro: Produto não encontrado!")
        return

    query = 'UPDATE estoque SET'
    params = []

    if tipo:
        query += ' tipo = ?,'
        params.append(tipo)
    if marca:
        query += ' marca = ?,'
        params.append(marca)
    if modelo:
        query += ' modelo = ?,'
        params.append(modelo)
    if quantidade is not None:
        query += ' quantidade = ?,'
        params.append(quantidade)
    if preco is not None:
        query += ' preco = ?,'
        params.append(preco)

    query = query.rstrip(',')
    query += ' WHERE serie = ?'
    params.append(serie)

    try:
        cursor.execute(query, tuple(params))
        conn.commit()
        print("Produto atualizado com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao atualizar o produto: {e}")

# ---------------------------------------------------------------------------
# Função: excluir_produto(serie)
# Descrição: Exclui um produto do estoque com base na série informada.
#           Valida se o produto existe antes de tentar a exclusão.
# ---------------------------------------------------------------------------
def excluir_produto(serie):
    if not produto_existe(serie):
        print("Erro: Produto não encontrado!")
        return
    cursor.execute('DELETE FROM estoque WHERE serie = ?', (serie,))
    conn.commit()
    print("Produto excluído do estoque com sucesso!")

# ---------------------------------------------------------------------------
# Função: consultar_produto_por_serie(serie)
# Descrição: Consulta e retorna um produto específico do estoque com base na série.
# ---------------------------------------------------------------------------
def consultar_produto_por_serie(serie):
    cursor.execute('SELECT * FROM estoque WHERE serie = ?', (serie,))
    produto = cursor.fetchone()
    return produto

# ---------------------------------------------------------------------------
# Função: consultar_produto_por_tipo(tipo)
# Descrição: Consulta e imprime todos os produtos do estoque que possuem o tipo informado.
# Se nenhum produto for encontrado, exibe mensagem correspondente.
# ---------------------------------------------------------------------------
def consultar_produto_por_tipo(tipo):
    cursor.execute('SELECT * FROM estoque WHERE tipo = ?', (tipo,))
    produtos = cursor.fetchall()
    if produtos:
        for produto in produtos:
            print(produto)
    else:
        print("Nenhum produto encontrado para esse tipo.")
