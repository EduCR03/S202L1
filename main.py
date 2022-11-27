from pprintpp import pprint as pp
from database import Graph

class Client(object):
    def __init__(self):
        self.db = Graph(uri='bolt://18.212.180.52:7687', user='neo4j', password='accordance-odds-breaths')

    def create_client(self, cliente):
        self.db.execute_query(
            'CREATE (c:Cliente{nome:$nome, data_nasc:$data_nasc, cpf:$cpf, agencia:$agencia}) return c',
            {'nome': cliente['nome'], 'data_nasc': cliente['data_nasc'], 'cpf': cliente['cpf'],
             'agencia': cliente['agencia']})
        return "CLIENTE CRIADO COM SUCESSO"

    def show_client(self, cliente):
        return self.db.execute_query('MATCH(c:Cliente{nome:$nome})  RETURN c',
                                     {'nome': cliente['nome']})

class Conta(object):
    def __init__(self):
        self.db = Graph(uri='bolt://18.212.180.52:7687', user='neo4j', password='accordance-odds-breaths')

    def create_conta(self, conta):
        aux_cliente = self.db.execute_query('MATCH(c:Cliente{nome:$nome}) RETURN c.nome',
                                            {'nome': conta['nome']})
        aux_funcionario = self.db.execute_query('MATCH(c:Funcionario{nome:$nome}) RETURN c.nome',
                                                {'nome': conta['nome']})
        if aux_cliente and aux_funcionario is not None:
            self.db.execute_query(
                'CREATE(t:Conta{nome:$nome, n_da_conta:$n_da_conta, valor:$valor, gerente:$gerente, '
                'tipo_da_conta:$tipo_da_conta}) return t',
                {'nome': conta['nome'], 'n_da_conta': conta['n_da_conta'], 'valor': conta['valor'],
                 'gerente': conta['gerente'], 'tipo_da_conta': conta['tipo_da_conta']})

            self.db.execute_query(
                'MATCH (c:Cliente{nome:$nome}), (t:Conta{n_da_conta:$n_da_conta}) CREATE (c)-[:POSSUI]->(t) RETURN c,t',
                {'nome': conta['nome'], 'n_da_conta': conta['n_da_conta']})

            self.db.execute_query(
                'MATCH (f:Funcionario{nome:$nome}), (t:Conta{n_da_conta:$n_da_conta}) CREATE (f)-[:GERENCIA]->(t) '
                'RETURN f,t',
                {'nome': conta['gerente'], 'n_da_conta': conta['n_da_conta']})

            return "CONTA CRIADA COM SUCESSO"
        else:
            return "CLIENTE OU FUNCIONARIO INVÁLIDOS, POR FAVOR TENTE NOVAMENTE"

    def fechar_conta(self, conta):
        self.db.execute_query('MATCH(t:Conta{n_da_conta:$n_da_conta}) DETACH DELETE t',
                              {'n_da_conta': conta['n_da_conta']})
        return "FECHAMENTO FEITO COM SUCESSO"

    def show_conta(self, conta):
        return self.db.execute_query('MATCH(t:Conta{n_da_conta: $n_da_conta}) RETURN t',
                                     {'n_da_conta': conta['n_da_conta']})


class Funcionario(object):
    def __init__(self):
        self.db = Graph(uri='bolt://18.212.180.52:7687', user='neo4j', password='accordance-odds-breaths')

    def create_funcionario(self, funcionario):
        self.db.execute_query(
            'CREATE (f:Funcionario{nome:$nome, funcao:$funcao, salario:$salario, matricula:$matricula}) RETURN f',
            {'nome': funcionario['nome'], 'funcao': funcionario['funcao'], 'salario': funcionario['salario'],
             'matricula': funcionario['matricula']})
        return "FUNCIONARIO CONTRATADO COM SUCESSO"

    def dar_aumento(self, funcionario):
        self.db.execute_query('MATCH(f:Funcionario{nome:$nome}) SET f.salario = $newsalario RETURN f',
                              {'nome': funcionario['nome'], 'newsalario': funcionario['new_salario']})
        return "AUMENTO REALIZADO COM SUCESSO"

    def demitir(self, funcionario):
        self.db.execute_query('MATCH(f:Funcionario{nome:$nome}) DETACH DELETE f',
                              {'nome': funcionario['nome']})
        return "FUNCIONARIO DEMITIDO COM SUCESSO"

    def show_funcionario(self, funcionario):
        return self.db.execute_query('MATCH(f:Funcionario{nome:$nome}) RETURN f',
                                     {'nome': funcionario['nome']})


class Caixa(object):
    def __init__(self):
        self.db = Graph(uri='bolt://44.198.166.226:7687', user='neo4j', password='comparison-farms-plays')

    def sacar_conta(self, atm):
        self.db.execute_query('MATCH(t:Conta) WHERE t.n_da_conta = $n_da_conta SET t.valor = t.valor-$valor RETURN t',
                                  {'n_da_conta': atm['n_da_conta'], 'valor': atm['valor']})
        return "SAQUE REALIZADO COM SUCESSO"


    def depositar_conta(self, atm):
        self.db.execute_query('MATCH(t:Conta) WHERE t.n_da_conta = $n_da_conta SET t.valor = t.valor+($valor) RETURN t',
                              {'n_da_conta': atm['n_da_conta'], 'valor': atm['valor']})
        return "DEPOSITO REALIZADO COM SUCESSO"

    def transferir_conta(self, atm):
        self.db.execute_query(
            'MATCH(o:Conta{n_da_conta:$n_da_conta_orig}),(d:Conta{n_da_conta:$n_da_conta_dest}) SET o.valor = '
            'o.valor-($valor), d.valor = d.valor+($valor) return o,d',
            {'n_da_conta_orig': atm['n_da_conta_orig'], 'n_da_conta_dest': atm['n_da_conta_dest'],
             'valor': atm['valor']})
        return "TRANSFERENCIA REALIZADA COM SUCESSO"

    def show_conta(self, atm):
        return self.db.execute_query('MATCH(t:Conta{n_da_conta: $n_da_conta}) RETURN t',
                                     {'n_da_conta': atm['n_da_conta']})


def divider():
    print('\n' + '-' * 80 + '\n')

while 1:
    cont_n_de_conta = 0
    client = Client()
    cont = Conta()
    func = Funcionario()
    atm = Caixa()
    option = input('1. Área do Cliente\n2. Área das Conta\n3. Área dos funcionários\n4. Caixa eletrônico\n')
    match option:
        case '1':
            option_cliente = input('\n1. Novo Cliente\n2. Mostrar informação\n')
            match option_cliente:

                case '1':
                    nome = input('Nome: ')
                    data_nasc = input('Data de nascimento: ')
                    cpf = input('CPF: ')
                    agencia = input('Agência: ')
                    cliente = {
                        'nome': nome,
                        'data_nasc': data_nasc,
                        'cpf': cpf,
                        'agencia': agencia
                    }
                    aux = client.create_client(cliente)
                    pp(aux)
                    divider()
                case '2':
                    nome = input('Nome do Cliente: ')
                    cliente = {
                        'nome': nome
                    }
                    aux = client.show_client(cliente)
                    pp(aux)
                    divider()
                case _:
                    pp("OPÇÃO INVALIDA")

        case '2':
            option_conta = input(
                '\n1. Criar conta\n2. Fechar conta\n3. Mostrar infos\n')
            match option_conta:
                case '1':
                    nome = input('Nome do Cliente: ')
                    n_da_conta = input('Nº da Conta: ')
                    dinheiro_inical = input('Quantidade de dinheiro inicial: ')
                    gerente = input('Gerente Responsável: ')
                    tipo_da_conta = input('Tipo de Conta: ')
                    conta = {
                        'nome': nome,
                        'n_da_conta': n_da_conta,
                        'valor': float(dinheiro_inical),
                        'gerente': gerente,
                        'tipo_da_conta': tipo_da_conta
                    }
                    aux = cont.create_conta(conta)
                    pp(aux)
                    divider()
                case '2':
                    n_da_conta = input("Nº da conta: ")
                    conta = {
                        'n_da_conta': n_da_conta
                    }
                    aux = cont.fechar_conta(conta)
                    pp(aux)
                    divider()
                case '3':
                    n_da_conta = input("Nº da conta: ")
                    conta = {
                        'n_da_conta': n_da_conta
                    }
                    aux = cont.show_conta(conta)
                    pp(aux)
                    divider()

        case '3':
            option_func = input("\n1. Contratar novo funcionário \n2. Aumentar salário \n3. Demitir \n4. Mostrar info "
                                "\n")
            match option_func:
                case '1':
                    nome = input("Nome: ")
                    funcao = input("Função: ")
                    salario = input("Salário inicial: ")
                    matricula = input("Matricula: ")
                    funcionario = {
                        'nome': nome,
                        'funcao': funcao,
                        'salario': float(salario),
                        'matricula': matricula
                    }
                    aux = func.create_funcionario(funcionario)
                    pp(aux)
                    divider()
                case '2':
                    nome = input('Nome: ')
                    new_salario = input("Novo salário: ")
                    funcionario = {
                        'nome': nome,
                        'new_salario': new_salario
                    }
                    aux = func.dar_aumento(funcionario)
                    pp(aux)
                    divider()
                case '3':
                    nome = input("Nome: ")
                    funcionario = {
                        'nome': nome
                    }
                    aux = func.demitir(funcionario)
                    pp(aux)
                    divider()
                case '4':
                    nome = input("Nome: ")
                    funcionario = {
                        'nome': nome
                    }
                    aux = func.show_funcionario(funcionario)
                    pp(aux)
                    divider()

        case '4':
            option_caixa = input(
                "\n1. Sacar da conta\n2. Depositar na conta\n3. Transferir para outra conta\n4. Mostrar saldo\n")
            match option_caixa:
                case '1':
                    n_da_conta = input("Nº da conta: ")
                    valor = input("Valor: ")
                    conta = {
                        'n_da_conta': n_da_conta,
                        'valor': float(valor)
                    }
                    aux = atm.sacar_conta(conta)
                    pp(aux)
                    divider()
                case '2':
                    n_da_conta = input("Nº da conta: ")
                    valor = input("Valor: ")
                    conta = {
                        'n_da_conta': n_da_conta,
                        'valor': float(valor)
                    }
                    aux = atm.depositar_conta(conta)
                    pp(aux)
                    divider()
                case '3':
                    n_da_conta_orig = input("Nº da conta de origem: ")
                    n_da_conta_dest = input("Nº da conta de destino: ")
                    valor = input("Valor: ")
                    conta = {
                        'n_da_conta_orig': n_da_conta_orig,
                        'n_da_conta_dest': n_da_conta_dest,
                        'valor': float(valor)
                    }
                    aux = atm.transferir_conta(conta)
                    pp(aux)
                    divider()
                case '4':
                    n_da_conta = input("Nº da conta: ")
                    conta = {
                        'n_da_conta': n_da_conta
                    }
                    aux = cont.show_conta(conta)
                    pp(aux)
                    divider()
