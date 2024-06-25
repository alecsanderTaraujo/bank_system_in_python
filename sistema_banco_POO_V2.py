import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

    @property
    @abstractmethod
    def valor(self):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("Operação falhou! Saldo insuficiente revise o Valor de Saldo Disponivel na Conta.")
            return False

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("Operação Falhou! O Valor Informado é Invalido, Valor minimo de Saque R$ 1,00.")
            return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito Realizado com Sucesso! Obrigado por usar nosso Banco!")
            return True

        else:
            print("Operação Falhou! Valor Informado Invalido, Valor minimo de Depósito R$ 1,00.")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("Operação falhou! Excedeu o limite do Valor de Saque.")
            return False

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")
            return False

        else:
            return super().sacar(valor)

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Banco:
    def __init__(self):
        self.clientes = []
        self.contas = []

    def criar_conta(self):
        cpf = input("Informe o CPF do usuário: \n ")
        cliente = self.filtrar_cliente(cpf)

        if cliente:
            numero_conta = len(self.contas) + 1
            conta = ContaCorrente(numero_conta, cliente)
            cliente.adicionar_conta(conta)
            self.contas.append(conta)
            print("Conta Criada com Sucesso")
        else:
            print("Usuário não encontrado, CPF não é nosso cliente. Erro ao Criar Conta. \n")

    def criar_usuario(self):
        cpf = input("Digite o CPF (somente números) que deseja cadastrar: \n ")
        cliente = self.filtrar_cliente(cpf)

        if cliente:
            print("CPF Informado já possui uma conta conosco, verifique os dados ou entre em contato com o Banco. \n")
            return None

        nome = input("Digite Seu Nome Completo: \n")
        data_de_nascimento = input("Digite sua Data de Nascimento (dd-mm-aaaa): \n")
        endereco = input("Informe o Endereço: logradouro, Número, bairro, cidade/sigla estado: \n")

        cliente = PessoaFisica(nome, data_de_nascimento, cpf, endereco)
        self.clientes.append(cliente)
        print("=== Usuário criado com sucesso! ===")
        return cliente

    def listar_contas(self):
        for conta in self.contas:
            print("=" * 100)
            print(str(conta))

    def filtrar_cliente(self, cpf):
        for cliente in self.clientes:
            if cliente.cpf == cpf:
                return cliente
        return None


def menu():
    menu = """\n
    ====== BEM VINDO AO SISTEMA DO BANCO ======
    [1]\tDEPÓSITO
    [2]\tSACAR
    [3]\tEXTRATO
    [4]\tCONFIGURAR LIMITE VALOR DE SAQUE
    [5]\tCONFIGURAR LIMITE DE SAQUE
    [6]\tNOVA CONTA
    [7]\tNOVO USUARIO
    [8]\tLISTAR CONTAS
    [0]\tSAIR

    Digite Opção Desejada:
    => """
    return input(textwrap.dedent(menu))


def main():
    banco = Banco()

    while True:
        opcao = menu()

        if opcao == "1":
            cpf = input("Informe o CPF do usuário: \n")
            cliente = banco.filtrar_cliente(cpf)
            if cliente:
                conta = recuperara_conta_cliente(cliente)
                if conta:
                    valor = float(input("Informe o Valor que Deseja Depósitar: \n"))
                    transacao = Deposito(valor)
                    cliente.realizar_transacao(conta, transacao)
            else:
                print("Usuário não encontrado. \n")

        elif opcao == "2":
            cpf = input("Informe o CPF do usuário: \n")
            cliente = banco.filtrar_cliente(cpf)
            if cliente:
                conta = recuperara_conta_cliente(cliente)
                if conta:
                    valor = float(input("Informe o Valor que Deseja Sacar: \n"))
                    transacao = Saque(valor)
                    cliente.realizar_transacao(conta, transacao)
            else:
                print("Usuário não encontrado. \n")

        elif opcao == "3":
            cpf = input("Informe o CPF do usuário: \n")
            cliente = banco.filtrar_cliente(cpf)
            if cliente:
                conta = recuperara_conta_cliente(cliente)
                if conta:
                    print("\n --------EXTRATO--------")
                    for transacao in conta.historico.transacoes:
                        print(f"{transacao['data']} - {transacao['tipo']} - R$ {transacao['valor']:.2f}")
                    print(f"\nSaldo: R$ {conta.saldo:.2f}")
                    print("---------------------------")
            else:
                print("Usuário não encontrado. \n")

        elif opcao == "4":
            cpf = input("Informe o CPF do usuário: \n")
            cliente = banco.filtrar_cliente(cpf)
            if cliente:
                conta = recuperara_conta_cliente(cliente)
                if conta:
                    limite = float(input("Informe o novo limite de saque: \n"))
                    conta.limite = limite
                    print(f"Novo limite de saque configurado para R$ {limite:.2f}")
            else:
                print("Usuário não encontrado. \n")

        elif opcao == "5":
            cpf = input("Informe o CPF do usuário: \n")
            cliente = banco.filtrar_cliente(cpf)
            if cliente:
                conta = recuperara_conta_cliente(cliente)
                if conta:
                    limite_saques = int(input("Informe o novo limite de número de saques: \n"))
                    conta.limite_saques = limite_saques
                    print(f"Novo limite de número de saques configurado para {limite_saques} saques")
            else:
                print("Usuário não encontrado. \n")

        elif opcao == "6":
            banco.criar_conta()

        elif opcao == "7":
            banco.criar_usuario()

        elif opcao == "8":
            banco.listar_contas()

        elif opcao == "0":
            print("OBRIGADO POR SER O NOSSO CLIENTE!!!")
            break

        else:
            print("Opção Invalida, por favor selecione novamente a opção desejada!")


def recuperara_conta_cliente(cliente):
    if not cliente.contas:
        print("Usuário não encontrado, CPF não é nosso cliente. Erro ao Acessar Conta. \n")
        return None
    # FIXME: NÃO PERMITE CLIENTE ESCOLHER A CONTA
    return cliente.contas[0]


main()
