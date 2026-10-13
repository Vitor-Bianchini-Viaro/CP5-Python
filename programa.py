import json

NOME_SISTEMA = "Loja Virtual MiniShop"
ARQ_JSON = "ocorrencias.json"
ARQ_DIARIO = "diario.txt"
ARQ_PASSAGEM = "passagem.txt"


def carregar_ocorrencias():
    try:
        with open(ARQ_JSON, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        dados = None

    if not isinstance(dados, list):
        print("ERRO: o arquivo ocorrencias.json está inválido (conteúdo não é uma lista JSON).")
        print("Corrija o arquivo manualmente (ele foi preservado) e tente novamente.")
        print("Cadastro, consulta de ocorrências e passagem de plantão ficam suspensos até lá.")
        return None
    return dados


def salvar_ocorrencias(lista):
    with open(ARQ_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(lista, arquivo, ensure_ascii=False, indent=4)


def ler_texto(mensagem):
    texto = input(mensagem).strip()
    while texto == "":
        print("O campo não pode ficar vazio.")
        texto = input(mensagem).strip()
    return texto


def ler_opcao(mensagem, validas):
    valor = input(mensagem).strip().lower()
    while valor not in validas:
        print("Valor inválido. Use: " + ", ".join(validas))
        valor = input(mensagem).strip().lower()
    return valor


def registrar_ocorrencia():
    lista = carregar_ocorrencias()
    if lista is None:
        return

    servico = ler_texto("Serviço afetado: ")
    descricao = ler_texto("Descrição (problema e efeito para o usuário): ")
    prioridade = ler_opcao("Prioridade (alta/media/baixa): ", ["alta", "media", "baixa"])
    status = ler_opcao("Status (aberto/resolvido): ", ["aberto", "resolvido"])
    if status == "resolvido":
        proxima_acao = "nenhuma"
    else:
        proxima_acao = ler_texto("Próxima ação para a próxima equipe: ")

    ocorrencia = {
        "servico": servico,
        "descricao": descricao,
        "prioridade": prioridade,
        "status": status,
        "proxima_acao": proxima_acao,
    }

    lista = carregar_ocorrencias()  # recarrega antes de incluir
    if lista is None:
        return
    lista.append(ocorrencia)
    salvar_ocorrencias(lista)
    print("Ocorrência registrada com sucesso.")


def consultar_ocorrencias():
    lista = carregar_ocorrencias()
    if lista is None:
        return
    if len(lista) == 0:
        print("Não há ocorrências registradas.")
        return
    numero = 1
    for ocorrencia in lista:
        print("--- Ocorrência " + str(numero) + " ---")
        print("Serviço: " + ocorrencia["servico"])
        print("Descrição: " + ocorrencia["descricao"])
        print("Prioridade: " + ocorrencia["prioridade"])
        print("Status: " + ocorrencia["status"])
        print("Próxima ação: " + ocorrencia["proxima_acao"])
        numero += 1


def registrar_diario():
    servico = ler_texto("Serviço: ")
    anotacao = ler_texto("Anotação: ")
    with open(ARQ_DIARIO, "a", encoding="utf-8") as arquivo:
        arquivo.write(servico + " — " + anotacao + "\n")
    print("Anotação registrada no diário.")


def consultar_diario():
    try:
        with open(ARQ_DIARIO, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
    except FileNotFoundError:
        print("Nenhuma anotação registrada")
        return
    if conteudo.strip() == "":
        print("Nenhuma anotação registrada")
    else:
        print("=== Diário ===")
        print(conteudo)


def gerar_passagem():
    lista = carregar_ocorrencias()
    if lista is None:
        print("Passagem de plantão não gerada; o resumo anterior foi preservado.")
        return

    abertas = []
    altas = 0
    for ocorrencia in lista:
        if ocorrencia["status"] == "aberto":
            abertas.append(ocorrencia)
            if ocorrencia["prioridade"] == "alta":
                altas += 1

    texto = "PASSAGEM DE PLANTÃO - " + NOME_SISTEMA + "\n"
    texto += "Ocorrências abertas: " + str(len(abertas)) + "\n"
    texto += "Abertas com prioridade alta: " + str(altas) + "\n"
    if len(abertas) == 0:
        texto += "Nenhuma pendência para o próximo plantão\n"
    else:
        texto += "\nPendências:\n"
        for ocorrencia in abertas:
            texto += "\nServiço: " + ocorrencia["servico"] + "\n"
            texto += "Descrição: " + ocorrencia["descricao"] + "\n"
            texto += "Prioridade: " + ocorrencia["prioridade"] + "\n"
            texto += "Próxima ação: " + ocorrencia["proxima_acao"] + "\n"

    with open(ARQ_PASSAGEM, "w", encoding="utf-8") as arquivo:
        arquivo.write(texto)

    with open(ARQ_PASSAGEM, "r", encoding="utf-8") as arquivo:
        print(arquivo.read())


def menu():
    opcao = ""
    while opcao != "6":
        print("\n=== Passagem de Plantão - " + NOME_SISTEMA + " ===")
        print("1 - Registrar ocorrência")
        print("2 - Consultar ocorrências")
        print("3 - Registrar anotação no diário")
        print("4 - Consultar diário")
        print("5 - Gerar passagem de plantão")
        print("6 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            registrar_ocorrencia()
        elif opcao == "2":
            consultar_ocorrencias()
        elif opcao == "3":
            registrar_diario()
        elif opcao == "4":
            consultar_diario()
        elif opcao == "5":
            gerar_passagem()
        elif opcao == "6":
            print("Encerrando o programa.")
        else:
            print("Opção inválida. Escolha um número de 1 a 6.")


menu()
