class ExpConstNumero:
    def __init__(self, valor: int) -> None:
        self.valor = valor
        self.tag = 'Número'
        

class ExpConstOperadorUnario:
    def __init__(self, operador: str, expressao) -> None:
        self.operador = operador
        self.expressao = expressao
        self.tag = 'Unário'
        

class ExpConstOperadorBinario:
    def __init__(self, esquerda, operador: str, direita) -> None:
        self.operador = operador
        self.esquerda = esquerda
        self.direita = direita
        self.tag = 'Binário'
        


class ExpConstFuncoes:
    def __init__(self, expressao, funcao) -> None:
        self.funcao = funcao
        self.expressao = expressao
        self.tag = 'Função'
        

class ExpConstParenteses:
    def __init__(self, expressao) -> None:
        self.expressao = expressao
        self.tag = 'Parênteses'
        

class ExpConstVariavel:
    def __init__(self, nome) -> None:
        self.nome = nome
        self.tag = 'Variável'
        

class ExpVazia:
    def __init__(self) -> None:
        self.tag = 'Vazia'


#Tarefa 0: 1 + 2 * 3 = 7
expressao_zero = ExpConstOperadorBinario(ExpConstNumero(1), '+', ExpConstOperadorBinario(ExpConstNumero(2), '*', ExpConstNumero(3)))
expressao_um = ExpConstOperadorBinario(ExpConstOperadorBinario(ExpConstNumero(1), '+', ExpConstNumero(2)), '*', ExpConstNumero(3))


contas = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b
}

def avaliar(expressao, dicionario_variaveis):
    match expressao.tag:
        case 'Binário':
            return contas[expressao.operador](avaliar(expressao.esquerda), avaliar(expressao.direita))
        case 'Unário':
            pass
        case 'Número':
            return expressao.valor
        case 'Parênteses':
            pass
        case 'Vazio':
            pass
        case 'Variável':
            return dicionario_variaveis[expressao.nome]
        case 'Função':
            pass
        case _:
            assert(0)

def to_string(expressao):
    match expressao.tag:
        case 'Binário':
            return '(' + str(to_string(expressao.esquerda)) + expressao.operador + str(to_string(expressao.direita)) + ')'
        case 'Unário':
            pass
        case 'Número':
            return expressao.valor
        case 'Parênteses':
            pass
        case 'Vazio':
            pass
        case 'Variável':
            pass
        case 'Função':
            pass
        case _:
            assert(0) 


print(eval(to_string(expressao_zero)))
print(eval(to_string(expressao_um)))