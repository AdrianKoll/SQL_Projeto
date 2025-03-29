from cliente_def import cadastrar_produto, listar_produtos_cliente, buscar_produto, atualizar_produto, deletar_produto
from estoque_df import produto_existe, adicionar_produto, listar_produtos as listar_estoque, \
    atualizar_produto as atualizar_estoque, excluir_produto, consultar_produto_por_serie, consultar_produto_por_tipo
from datetime import datetime


# Função para validar entradas numéricas
def validar_numero_input(prompt, tipo=float, valor_default=None):
    while True:
        try:
            valor = input(prompt)
            if valor == "" and valor_default is not None:
                return valor_default
            return tipo(valor)
        except ValueError:
            print("Valor inválido. Por favor, insira um número válido.")

# Função para cancelar a compra e retornar a quantidade ao estoque
def cancelar_compra(serie, quantidade_cancelada, preco_unitario):
    resultado = consultar_produto_por_serie(serie)
    if resultado:
        estoque_atual = resultado[4]
        # Atualiza o estoque, somando de volta a quantidade cancelada
        novo_estoque = estoque_atual + quantidade_cancelada
        atualizar_estoque(serie, resultado[1], resultado[2], resultado[3], novo_estoque, preco_unitario)
        print(f"Compra cancelada. {quantidade_cancelada} unidades retornaram ao estoque.")
    else:
        print("Erro: Produto não encontrado no estoque.")

# Menu para interação com o usuário
def menu():
    while True:
        print(
            "\n[1] Cadastrar Produto\n[2] Listar Produtos\n[3] Buscar Produto\n[4] Atualizar Produto\n[5] Deletar Produto\n[6] Adicionar ao Estoque\n[7] Listar Estoque\n[8] Atualizar Estoque\n[9] Excluir do Estoque\n[10] Consultar por Tipo\n[11] Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cpf = input("CPF (obrigatório): ").strip()
            nome = input("Nome (obrigatório): ").strip()
            data_nascimento = input("Data de nascimento (AAAA-MM-DD, obrigatório): ").strip()
            categoria = input("Categoria (obrigatório): ").strip()
            serie = input("Série (obrigatório): ").strip()
            tipo = input("Tipo (obrigatório): ").strip()
            marca = input("Marca (obrigatório): ").strip()

            quantidade = validar_numero_input("Quantidade (obrigatório): ", tipo=int)

            # Busca o produto pelo número de série no estoque
            resultado = consultar_produto_por_serie(serie)
            if not resultado:
                print("Erro: Produto não encontrado no estoque.")
                continue

            preco_unitario_estoque = resultado[5]  # Preço do produto no estoque
            estoque_atual = resultado[4]

            if estoque_atual < quantidade:
                print("Erro: Quantidade insuficiente no estoque.")
                continue

            # Cálculo do valor total usando o preço do estoque
            preco_total = preco_unitario_estoque * quantidade  # Usar o preço do estoque para calcular o total
            print(f"\nDetalhes da Compra:")
            print(f"Preço Unitário (Estoque): R${preco_unitario_estoque:.2f}")
            print(f"Quantidade: {quantidade}")
            print(f"Total da Compra: R${preco_total:.2f}")

            # Confirmar a compra
            confirmar = input("Deseja confirmar a compra? (s/n): ").strip().lower()
            if confirmar != "s":
                print("Compra cancelada.")
                continue

            # Perguntar se o usuário deseja cancelar a compra após a confirmação
            cancelar = input(
                f"Você tem certeza que deseja cancelar a compra de {quantidade} unidades? O valor total seria R${preco_total:.2f}. (s/n): ").strip().lower()
            if cancelar == "s":
                # Cancela a compra e retorna a quantidade ao estoque
                cancelar_compra(serie, quantidade, preco_unitario_estoque)
                continue

            data_compra = input("Data da compra (AAAA-MM-DD HH:MM:SS) [Enter para atual]: ").strip()
            if not data_compra:
                data_compra = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Registra a compra com o preço correto do estoque
            cadastrar_produto(cpf, nome, categoria, serie, tipo, marca, quantidade, preco_total, data_compra,
                              data_nascimento)

            # Atualiza o estoque com a quantidade comprada
            atualizar_estoque(serie, tipo, marca, categoria, estoque_atual - quantidade, preco_unitario_estoque)

        elif opcao == "2":
            listar_produtos_cliente()

        elif opcao == "3":
            cpf = input("Digite o CPF do produto: ")
            buscar_produto(cpf)

        elif opcao == "4":
            cpf = input("CPF do produto a ser atualizado: ").strip()
            nome = input("Novo Nome (Enter para manter): ").strip() or None
            data_nascimento = input("Nova Data de Nascimento (AAAA-MM-DD) [Enter para manter]: ").strip() or None
            categoria = input("Nova Categoria (Enter para manter): ").strip() or None
            serie = input("Nova Série (Enter para manter): ").strip() or None
            tipo = input("Novo Tipo (Enter para manter): ").strip() or None
            marca = input("Nova Marca (Enter para manter): ").strip() or None

            quantidade = input("Nova Quantidade (Enter para manter): ").strip()
            quantidade = int(quantidade) if quantidade else None

            preco = input("Novo Preço (Enter para manter): ").strip()
            preco = float(preco) if preco else None

            data_compra = input("Nova Data da compra (AAAA-MM-DD HH:MM:SS) [Enter para manter]: ").strip() or None

            atualizar_produto(cpf, nome, data_nascimento, categoria, serie, tipo, marca, quantidade, preco, data_compra)

        elif opcao == "5":
            cpf = input("Digite o CPF do produto a ser excluído: ")
            deletar_produto(cpf)

        elif opcao == "6":
            serie = input("Digite a série do produto (obrigatório): ").strip()
            tipo = input("Digite o tipo do produto (obrigatório): ").strip()
            marca = input("Digite a marca do produto (obrigatório): ").strip()
            categoria = input("Digite a categoria do produto (obrigatório): ").strip()

            quantidade = validar_numero_input("Digite a quantidade do produto: ", tipo=int)
            preco = validar_numero_input("Digite o preço do produto: ", tipo=float)

            if produto_existe(serie):
                atualizar_estoque(serie, tipo, marca, categoria, quantidade, preco)
            else:
                adicionar_produto(serie, tipo, marca, categoria, quantidade, preco)

        elif opcao == "7":
            listar_estoque()

        elif opcao == "8":
            serie = input("Digite a série do produto a ser atualizado: ").strip()
            if not produto_existe(serie):
                print(f"Erro: Produto com série {serie} não encontrado no estoque.")
                continue

            tipo = input("Novo tipo (Enter para manter): ").strip() or None
            marca = input("Nova marca (Enter para manter): ").strip() or None
            categoria = input("Nova categoria (Enter para manter): ").strip() or None

            quantidade = input("Nova quantidade (Enter para manter): ").strip()
            quantidade = int(quantidade) if quantidade else None

            preco = input("Novo preço (Enter para manter): ").strip()
            preco = float(preco) if preco else None

            atualizar_estoque(serie, tipo, marca, categoria, quantidade, preco)

        elif opcao == "9":
            serie = input("Digite a série do produto a ser excluído do estoque: ").strip()
            if produto_existe(serie):
                excluir_produto(serie)
                print("Produto excluído do estoque com sucesso!")
            else:
                print("Erro: Produto não encontrado no estoque.")

        elif opcao == "10":
            tipo = input("Digite o tipo de produto para consulta: ").strip()
            resultado = consultar_produto_por_tipo(tipo)
            if resultado:
                print("\nProdutos encontrados:")
                for produto in resultado:
                    print(f"Série: {produto[3]}, Tipo: {produto[1]}, Marca: {produto[2]}, Categoria: {produto[0]}")
            else:
                print("Nenhum produto encontrado para esse tipo.")

        elif opcao == "11":
            print("Saindo...")
            break

        else:
            print("Opção inválida! Tente novamente.")


if __name__ == "__main__":
    menu()
