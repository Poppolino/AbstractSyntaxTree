import math

variable = {}
class ExpConstOperadorBinario:
    def __init__(self, esquerda, operador: str, direita):
        self.esquerda = esquerda
        self.operador = operador
        self.direita = direita
        self.tag = "Binário"

class ExpConstNumero:
    def __init__(self, valor: str):
        self.valor = valor
        self.tag = "Número"

class ExpConstOperadorUnario:
    def __init__(self, operador: str, expressao):
        self.operador = operador
        self.expressao = expressao
        self.tag = "Unário"

class ExpConstVariavel:
    def __init__(self, nome: str):
        self.nome = nome
        self.tag = "Variável"

class ExpConstParenteses:
    def __init__(self, expressao):
        self.expressao = expressao
        self.tag = "Parênteses"

class ExpConstFuncoes:
    def __init__(self, nome: str, expressao: list):
        self.nome = "sqrt"
        self.expressao = expressao
        self.tag = "Função"

class ExpVazia:
    def __init__(self):
        self.tag = "Vazia"

class ExpConstAtribuicao:
    def __init__(self, nome: str, expressao):
        self.nome = nome
        self.expressao = expressao
        self.tag = "Atribuição"
        variable[nome] = expressao

class Token:
    def __init__(self, valor, tag: str):
        self.valor = valor
        self.tag = tag

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.indice = 0
        self.proximo_token = tokens[self.indice]
        
    def espiadinha(self, tag):
        return self.proximo_token.tag == tag
    
    def consome(self, tag):
        if self.espiadinha(tag):
            self.indice += 1
            self.proximo_token = self.tokens[self.indice]
            return self.tokens[self.indice - 1]
        else:
            raise SyntaxError('Tu é bobão!')
    
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

    def parserS(self):
        if self.espiadinha("VARIÁVEL"):
            return self.parserVS()
        elif self.espiadinha("IMPRESSÃO"):
            return self.parserPS()
        elif self.espiadinha("LINHA") or self.espiadinha("FIM"):
            return ExpVazia()
        else:
            raise SyntaxError('Tu é bobão!')

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




contas = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
}

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

def otimizar(expressao, variables = variable):
    match expressao.tag:
        case "Unário":
            if expressao.operador == "-":
                if expressao.expressao.tag == "Unário" and expressao.expressao.operador == "-":
                    return otimizar(expressao.expressao.expressao, variables)
            return ExpConstOperadorUnario(expressao.operador, otimizar(expressao.expressao, variables))
        case "Binário":
            if expressao.direita.tag == "Número" and expressao.direita.valor == 0:
                return otimizar(expressao.esquerda, variables)
            return ExpConstOperadorBinario(otimizar(expressao.esquerda, variables), expressao.operador, otimizar(expressao.direita, variables))
        case "Número":
            return expressao
        case "Variável":
            return otimizar(variables[expressao.nome], variables)
        case "Parênteses":
            return ExpConstParenteses(otimizar(expressao.expressao, variables))
        case "Função":
            return ExpConstFuncoes(expressao.nome, [otimizar(argument, variables) for argument in expressao.expressao])
        case "Vazia":
            return ExpVazia()
        case "Atribuição":
            return ExpConstAtribuicao(expressao.nome, otimizar(expressao.expressao, variables))
        case _:
            raise SyntaxError('Tu é bobão!')