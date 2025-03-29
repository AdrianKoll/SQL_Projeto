from def_database import cadastrar_produto, listar_produtos, buscar_produto, atualizar_produto, deletar_produto
from datetime import datetime

def menu():
    while True:
        print(
            "\n[1] Cadastrar Produto\n[2] Listar Produtos\n[3] Buscar Produto\n[4] Atualizar Produto\n[5] Deletar Produto\n[6] Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            while True:
                cpf = input("CPF (obrigatório): ")
                if cpf:
                    break
                print("Erro: O CPF é obrigatório.")

            while True:
                nome = input("Nome (obrigatório): ")
                if nome:
                    break
                print("Erro: O nome é obrigatório.")

            # Perguntar pela data de nascimento logo após o nome
            while True:
                data_nascimento = input("Data de nascimento (AAAA-MM-DD, obrigatório): ")
                try:
                    # Validar formato da data
                    datetime.strptime(data_nascimento, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Erro: A data deve estar no formato AAAA-MM-DD.")

            while True:
                categoria = input("Categoria (obrigatório): ")
                if categoria:
                    break
                print("Erro: A categoria é obrigatória.")

            # Valida entrada para quantidade (inteiro)
            while True:
                try:
                    quantidade = int(input("Quantidade (obrigatório): "))
                    break
                except ValueError:
                    print("Erro: A quantidade deve ser um número inteiro válido.")

            # Valida entrada para preço (float)
            while True:
                try:
                    preco = float(input("Preço (obrigatório): "))
                    break
                except ValueError:
                    print("Erro: O preço deve ser um número válido (ex: 10.50).")

            # Perguntar pela data da compra
            while True:
                data_compra = input("Data da compra (AAAA-MM-DD HH:MM:SS) [Enter para usar a atual]: ")
                data_compra = data_compra.strip() if data_compra else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if data_compra:
                    break
                print("Erro: A data da compra é obrigatória.")

            # Chama a função de cadastro
            cadastrar_produto(cpf, nome, categoria, quantidade, preco, data_compra, data_nascimento)

        elif opcao == "2":
            listar_produtos()

        elif opcao == "3":
            cpf = input("Digite o CPF do produto: ")
            buscar_produto(cpf)

        elif opcao == "4":
            cpf = input("CPF do produto a ser atualizado: ")
            nome = input("Novo Nome (Enter para manter): ")

            # Perguntar se deseja fornecer nova data de nascimento
            data_nascimento = input("Nova Data de Nascimento (AAAA-MM-DD) [Enter para manter]: ")
            data_nascimento = data_nascimento.strip() if data_nascimento else None

            # Perguntar se deseja fornecer nova categoria
            categoria = input("Nova Categoria (Enter para manter): ")

            # Valida a quantidade se fornecida
            quantidade = input("Nova Quantidade (Enter para manter): ")
            quantidade = int(quantidade) if quantidade.strip() else None

            # Valida o preço se fornecido
            preco = input("Novo Preço (Enter para manter): ")
            preco = float(preco) if preco.strip() else None

            # Perguntar pela nova data de compra
            data_compra = input("Nova Data da compra (AAAA-MM-DD HH:MM:SS) [Enter para manter]: ")
            data_compra = data_compra.strip() if data_compra else None

            atualizar_produto(cpf, nome, data_nascimento, categoria, quantidade, preco, data_compra)

        elif opcao == "5":
            cpf = input("Digite o CPF do produto a ser excluído: ")
            deletar_produto(cpf)

        elif opcao == "6":
            print("Saindo...")
            break

        else:
            print("Opção inválida! Tente novamente.")


if __name__ == "__main__":
    menu()
