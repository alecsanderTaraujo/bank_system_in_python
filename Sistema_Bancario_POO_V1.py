from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self,endereco):
        self.endereco = endereco
        self.conta = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self,nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    
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

    def sacar(self,valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("Operação falhou! Saldo insuficiente revise o Valor de Saldo Disponivel na Conta.")

        elif valor > 0:
            self._saldo -= valor 
            print("\n=== Saque realizado com sucesso! ===")
            return True
        
        else:
            print("Operação Falhou! O Valor Informado é Invalido, Valor minimo de Saque R$ 1,00.")
            return False
        
    def depositar(self,valor):
        if valor > 0:
         self._saldo += valor 
         print("Depósito Realizado com Sucesso! Obrigado por usar nosso Banco!")

        else:
         print("Operação Falhou! Valor Informado Invalido, Valor minimo de Depósito R$ 1,00.")
         return False

        return True       
        

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao ["tipo"] == Saque.__name__])
        
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques
        
        if excedeu_limite:
            print("Operação falhou! Excedeu o limite do Valor de Saque.")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
    
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
                "data": datetime.now().strftime
                ("%d-%m-%Y %H:%M:%s"),
            }
        )

class Transacao(ABC):
    @property
    @abstractclassmethod
    def registrar(self,conta):
        pass

    @abstractproperty
    def valor(self):
        pass
    
class Saque(Transacao):
    def __int__(self, valor):
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