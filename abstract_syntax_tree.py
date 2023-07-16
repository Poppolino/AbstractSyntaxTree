import math

variable = {}

# Expressão para operações binárias
class ExpConstOperadorBinario:
    def __init__(self, esquerda, operador: str, direita):
        self.esquerda = esquerda
        self.operador = operador
        self.direita = direita
        self.tag = "Binário"

# Expressão para números
class ExpConstNumero:
    def __init__(self, valor: str):
        self.valor = valor
        self.tag = "Número"

# Expressão para operações unárias
class ExpConstOperadorUnario:
    def __init__(self, operador: str, expressao):
        self.operador = operador
        self.expressao = expressao
        self.tag = "Unário"

# Expressão para quando se usa o valor de uma variável 
class ExpConstVariavel:
    def __init__(self, nome: str):
        self.nome = nome
        self.tag = "Variável"

# Expressão para parênteses
class ExpConstParenteses:
    def __init__(self, expressao):
        self.expressao = expressao
        self.tag = "Parênteses"

# Expressão para funções (sqrt)
class ExpConstFuncoes:
    def __init__(self, nome: str, expressao: list):
        self.nome = "sqrt"
        self.expressao = expressao
        self.tag = "Função"

# Expressão Vazia
class ExpVazia:
    def __init__(self):
        self.tag = "Vazia"

# Uma dada expressão é atribuída a uma variável  
class ExpConstAtribuicao:
    def __init__(self, nome: str, expressao):
        self.nome = nome
        self.expressao = expressao
        self.tag = "Atribuição"
        variable[nome] = expressao


# Cada token é formado por um tipo (tag) e um valor (encontrado no texto) 
class Token:
    def __init__(self, valor, tag: str):
        self.valor = valor
        self.tag = tag



# Classe responsável pela análise sintática das expressões passadas como sequências de tokens
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.indice = 0
        self.proximo_token = tokens[self.indice]
    

    # Verifica se o próximo token é do tipo informado
    def espiadinha(self, tag):
        return self.proximo_token.tag == tag
    

    # Verifica o token e o consome, caso seja do tipo esperado.
    # Isso faz com que o "próximo token" seja atualizado. 
    def consome(self, tag):
        if self.espiadinha(tag):
            self.indice += 1
            self.proximo_token = self.tokens[self.indice]
            return self.tokens[self.indice - 1]
        else:
            raise SyntaxError('Tu é bobão!')
    

    # Gera a expressão com base nas regras:
    # VS -> 
    # VS -> VS <var> '=' E <newline>  
    def parserVS(self):
        e = ExpVazia()

        while True:
            if self.espiadinha("FIM"):
                return e
            elif self.espiadinha("VARIÁVEL"):
                var = self.consome("VARIÁVEL")
                self.consome("ATRIBUIÇÃO")
                exp = self.parserE()
                e = ExpConstAtribuicao(var.valor, exp)
                if not self.espiadinha("LINHA"):
                    if self.espiadinha("FIM"):
                        return e
                    raise SyntaxError('Tu é bobão!')
            else:
                break
        return e
    

    # Gera a expressão com base nas regras:
    # PS -> 
    # PS -> PS '@' E <newline>  
    def parserPS(self):
        e = ExpVazia()

        while True:
            if self.espiadinha("FIM"):
                return e
            elif self.espiadinha("IMPRESSÃO"):
                self.consome("IMPRESSÃO")
                e = self.parserE()
                if not self.espiadinha("LINHA"):
                    if self.espiadinha("FIM"):
                        return e
                    raise SyntaxError('Tu é bobão!')
            else:
                break
        return e


    # Gera a expressão com base na regra:
    # S -> VS PS
    def parserS(self):
        if self.espiadinha("VARIÁVEL"):
            return self.parserVS()
        elif self.espiadinha("IMPRESSÃO"):
            return self.parserPS()
        elif self.espiadinha("LINHA") or self.espiadinha("FIM"):
            return ExpVazia()
        else:
            raise SyntaxError('Tu é bobão!')


    # Gera a expressão com base nas regras:
    # E -> E '+' T
    # E -> E '-' T
    # E -> T
    def parserE(self):
        e = self.parserT()
        while True:
            if self.espiadinha("FIM"):
                return e
            elif self.espiadinha("SOMA"):
                self.consome("SOMA")
                e = ExpConstOperadorBinario(e, "+", self.parserT())
            elif self.espiadinha("SUBTRAÇÃO"):
                self.consome("SUBTRAÇÃO")
                e = ExpConstOperadorBinario(e, "-", self.parserT())
            else:
                break
        return e


    # Gera a expressão com base nas regras:
    # T -> T '*' F
    # T -> T '/' F
    # T -> F
    def parserT(self):
        e = self.parserF()
        while True:
            if self.espiadinha("FIM"):
                return e
            elif self.espiadinha("MULTIPLICAÇÃO"):
                self.consome("MULTIPLICAÇÃO")
                e = ExpConstOperadorBinario(e, "*", self.parserF())
            elif self.espiadinha("DIVISÃO"):
                self.consome("DIVISÃO")
                e = ExpConstOperadorBinario(e, "/", self.parserF())
            else:
                break
        return e
    

    # Gera a expressão com base nas regras:
    # F -> '-' F
    # F -> <num>
    # F -> <var>
    # F -> <sqrt> '(' E ')'
    # F -> '(' E ')'
    def parserF(self):
        if self.espiadinha("NÚMERO"):
            n = self.consome("NÚMERO")
            return ExpConstNumero(float(n.valor))
        
        elif self.espiadinha("VARIÁVEL"):
            v = self.consome("VARIÁVEL")
            return ExpConstVariavel(v.valor)
                        
        elif self.espiadinha("ABRE"):
            self.consome("ABRE")
            e = self.parserE()
            self.consome("FECHA")
            return ExpConstParenteses(e)
            
        elif self.espiadinha("SUBTRAÇÃO"):
            self.consome("SUBTRAÇÃO")
            e = self.parserF()
            return ExpConstOperadorUnario("-", e)
        
        elif self.espiadinha("RAIZ"):
            function = self.consome("RAIZ").valor
            if self.espiadinha("ABRE"):
                self.consome("ABRE")
                e = self.parserE()
                self.consome("FECHA")
                return ExpConstFuncoes(function, [e])


# Definição das operações matemáticas do nosso problema
contas = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
}


# Realiza o cálculo da expressão matemática passada e retorna o resultado
def avaliar(expressao, variables = variable):
    match expressao.tag:
        case 'Binário':
            return contas[expressao.operador](avaliar(expressao.esquerda), avaliar(expressao.direita))
        case "Número":
            return expressao.valor
        case "Unário":
            if expressao.operador == "-":
                return -avaliar(expressao.expressao, variables)
            else:
                raise Exception("Invalid Unário, got " + expressao.operador + " instead.")
        case "Variável":
            return avaliar(variables[expressao.nome], variables)
        case "Parênteses":
            return avaliar(expressao.expressao, variables)
        case "Função":
            return math.sqrt(avaliar(expressao.expressao[0], variables))
        case "Vazia":
            return 0
        case "Atribuição":
            return avaliar(expressao.expressao, variables) 
        case _:
            raise SyntaxError('Tu é bobão!')


# Constrói a string da expressão a ser resolvida
def expressao_string(expressao, variables = variable):
    match expressao.tag:
        case "Binário":
            return "(" + expressao_string(expressao.esquerda, variables) + " " + expressao.operador + " " + expressao_string(expressao.direita, variables) + ")"
        case "Número":
            return str(expressao.valor)       
        case "Unário":
            return "(" + expressao.operador + expressao_string(expressao.expressao, variables) + ")"
        case "Variável":
            return expressao_string(variables[expressao.nome], variables)
        case "Parênteses":
            return "(" + expressao_string(expressao.expressao, variables) + ")"
        case "Função":
            return "sqrt(" + ", ".join([expressao_string(argument, variables) for argument in expressao.expressao]) + ")"
        case "Vazia":
            return ""
        case "Atribuição":
            return expressao.nome + " = " + expressao_string(expressao.expressao, variables)
        case _:
            raise SyntaxError('Tu é bobão!')