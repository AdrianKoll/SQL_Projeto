
from cliente_def import cadastrar_produto, listar_produtos_cliente, atualizar_produto, deletar_produto
from estoque_def import produto_existe, adicionar_produto, listar_produtos as listar_estoque, \
    atualizar_produto as atualizar_estoque, excluir_produto, consultar_produto_por_serie
from datetime import datetime

# ---------------------------------------------------------------------------
# Função: validar_numero_input(prompt, tipo=float, valor_default=None)
# Descrição: Valida a entrada do usuário, garantindo que o valor fornecido
# seja do tipo especificado. Caso o usuário não forneça um valor (string vazia)
# e um valor_default seja definido, retorna o default.
# ---------------------------------------------------------------------------
def validar_numero_input(prompt, tipo=float, valor_default=None):
    while True:
        try:
            valor = input(prompt)
            if valor == "" and valor_default is not None:
                return valor_default
            return tipo(valor)
        except ValueError:
            print("Valor inválido. Por favor, insira um número válido.")

# ---------------------------------------------------------------------------
# Função: cancelar_compra(serie, quantidade_cancelada, preco_unitario)
# Descrição: Cancela a compra de um produto. Através da série do produto, recupera
# os dados do estoque, soma a quantidade cancelada de volta ao estoque e atualiza o registro.
# ---------------------------------------------------------------------------
def cancelar_compra(serie, quantidade_cancelada, preco_unitario):
    resultado = consultar_produto_por_serie(serie)
    if resultado:
        # Estrutura do estoque:
        # índice 0: série, 1: tipo, 2: marca, 3: modelo, 4: quantidade, 5: preço, 6: data/hora
        estoque_atual = resultado[4]
        novo_estoque = estoque_atual + quantidade_cancelada
        atualizar_estoque(serie, resultado[1], resultado[2], resultado[3], novo_estoque, preco_unitario)
        print(f"Compra cancelada. {quantidade_cancelada} unidades retornaram ao estoque.")
    else:
        print("Erro: Produto não encontrado no estoque.")

# ---------------------------------------------------------------------------
# Função: menu()
# Descrição: Exibe um menu interativo para o usuário realizar operações relacionadas
# ao cliente (vender, listar, atualizar e deletar) e ao estoque (adicionar, listar,
# atualizar e excluir). O menu utiliza o formato de datas DD/MM/AAAA e DD/MM/AAAA HH:MM:SS.
# ---------------------------------------------------------------------------
def menu():
    while True:
        print(
            "\nCLIENTE-----------"
            "\n[1] Vender"
            "\n[2] Listar"
            "\n[3] Atualizar"
            "\n[4] Deletar"
            "\n\nESTOQUE-----------"
            "\n[5] Adicionar"
            "\n[6] Listar"
            "\n[7] Atualizar"
            "\n[8] Deletar"
            "\n[9] Sair\n"
        )
        opcao = input("Escolha uma opção: ").strip()

        # -----------------------------------------------------------------------
        # Opção 1: Venda
        # Solicita informações do cliente e do produto, valida a existência e quantidade
        # no estoque e registra a compra utilizando datas no formato DD/MM/AAAA ou
        # DD/MM/AAAA HH:MM:SS.
        # -----------------------------------------------------------------------
        if opcao == "1":
            cpf = input("CPF: ").strip()
            nome = input("Nome: ").strip()
            data_nascimento = input("Data de nascimento (DD/MM/AAAA): ").strip()
            serie = input("Série: ").strip()
            tipo = input("Tipo: ").strip()
            marca = input("Marca: ").strip()
            modelo = input("Modelo: ").strip()

            quantidade = validar_numero_input("Quantidade (obrigatório): ", tipo=int)

            # Busca o produto pelo número de série no estoque
            resultado = consultar_produto_por_serie(serie)
            if not resultado:
                print("Erro: Produto não encontrado no estoque.")
                continue

            # Estrutura do estoque: [0]=série, [1]=tipo, [2]=marca, [3]=modelo, [4]=quantidade, [5]=preço, [6]=data/hora
            preco_unitario_estoque = int(resultado[5])
            estoque_atual = resultado[4]

            if estoque_atual < quantidade:
                print("Erro: Quantidade insuficiente no estoque.")
                continue

            preco_total = preco_unitario_estoque * quantidade
            print(f"\nDetalhes da Compra:")
            print(f"Preço Unitário (Estoque): R${preco_unitario_estoque:.2f}")
            print(f"Quantidade: {quantidade}")
            print(f"Total da Compra: R${preco_total:.2f}")

            confirmar = input("Deseja confirmar a compra? (s/n): ").strip().lower()
            if confirmar != "s":
                print("Compra cancelada.")
                continue

            # Utiliza o formato DD/MM/AAAA HH:MM:SS para a data da compra
            data_compra = input("Data da compra (DD/MM/AAAA HH:MM:SS) [Enter para atual]: ").strip()
            if not data_compra:
                data_compra = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            # Registra a compra
            cadastrar_produto(cpf, nome, serie, tipo, marca, modelo, quantidade, preco_unitario_estoque, data_compra, data_nascimento)

            # Atualiza o estoque
            atualizar_estoque(serie, tipo, marca, modelo, estoque_atual - quantidade, preco_unitario_estoque)

        # -----------------------------------------------------------------------
        # Opção 2: Listar produtos do cliente
        # -----------------------------------------------------------------------
        elif opcao == "2":
            listar_produtos_cliente()

        # -----------------------------------------------------------------------
        # Opção 3: Atualizar produto do cliente
        # -----------------------------------------------------------------------
        elif opcao == "3":
            cpf = input("CPF do produto a ser atualizado: ").strip()
            nome = input("Novo Nome (Enter para manter): ").strip() or None
            data_nascimento = input("Nova Data de Nascimento (DD/MM/AAAA) [Enter para manter]: ").strip() or None
            serie = input("Nova Série (Enter para manter): ").strip() or None
            tipo = input("Novo Tipo (Enter para manter): ").strip() or None
            marca = input("Nova Marca (Enter para manter): ").strip() or None
            modelo = input("Novo Modelo (Enter para manter): ").strip() or None

            quantidade = input("Nova Quantidade (Enter para manter): ").strip()
            quantidade = int(quantidade) if quantidade else None

            preco = input("Novo Preço (Enter para manter): ").strip()
            preco = float(preco) if preco else None

            data_compra = input("Nova Data da compra (DD/MM/AAAA HH:MM:SS) [Enter para manter]: ").strip() or None

            atualizar_produto(cpf, nome, data_nascimento, serie, tipo, marca, modelo, quantidade, preco, data_compra)

        # -----------------------------------------------------------------------
        # Opção 4: Deletar produto do cliente
        # -----------------------------------------------------------------------
        elif opcao == "4":
            cpf = input("Digite o CPF do produto a ser excluído: ").strip()
            deletar_produto(cpf)

        # -----------------------------------------------------------------------
        # Opção 5: Adicionar produto ao estoque
        # -----------------------------------------------------------------------
        elif opcao == "5":
            tipo = input("Digite o tipo do produto: ").strip()
            marca = input("Digite a marca do produto: ").strip()
            modelo = input("Digite o modelo do produto: ").strip()
            serie = input("Digite a série do produto: ").strip()

            quantidade = validar_numero_input("Digite a quantidade do produto: ", tipo=int)
            preco = validar_numero_input("Digite o preço do produto: ", tipo=float)

            if produto_existe(serie):
                atualizar_estoque(serie, tipo, marca, modelo, quantidade, preco)
            else:
                adicionar_produto(serie, tipo, marca, modelo, quantidade, preco)

        # -----------------------------------------------------------------------
        # Opção 6: Listar produtos do estoque
        # -----------------------------------------------------------------------
        elif opcao == "6":
            produtos = listar_estoque()
            if not produtos:
                print("Nenhum produto encontrado no estoque.")

        # -----------------------------------------------------------------------
        # Opção 7: Atualizar produto do estoque
        # -----------------------------------------------------------------------
        elif opcao == "7":
            serie = input("Digite a série do produto a ser atualizado: ").strip()
            if not produto_existe(serie):
                print(f"Erro: Produto com série {serie} não encontrado no estoque.")
                continue

            tipo = input("Novo Tipo (Enter para manter): ").strip() or None
            marca = input("Nova Marca (Enter para manter): ").strip() or None
            modelo = input("Novo Modelo (Enter para manter): ").strip() or None

            quantidade = input("Nova Quantidade (Enter para manter): ").strip()
            quantidade = int(quantidade) if quantidade else None

            preco = input("Novo Preço (Enter para manter): ").strip()
            preco = float(preco) if preco else None

            atualizar_estoque(serie, tipo, marca, modelo, quantidade, preco)

        # -----------------------------------------------------------------------
        # Opção 8: Excluir produto do estoque
        # -----------------------------------------------------------------------
        elif opcao == "8":
            serie = input("Digite a série do produto a ser excluído do estoque: ").strip()
            if produto_existe(serie):
                excluir_produto(serie)
            else:
                print("Erro: Produto não encontrado no estoque.")

        # -----------------------------------------------------------------------
        # Opção 9: Sair do sistema
        # -----------------------------------------------------------------------
        elif opcao == "9":
            print("Saindo...")
            break

        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()
