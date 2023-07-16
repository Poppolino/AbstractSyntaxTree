import math

class ExpressaoConstrutor:
    def __init__(self, tag: str) -> None:
        self.tag = tag

class OperadorUnario(ExpressaoConstrutor):
    def __init__(self, operador: str, expressao: ExpressaoConstrutor):
        super().__init__("Unário")
        self.operador = operador
        self.expressao = expressao
        
class OperadorBinario(ExpressaoConstrutor):
    def __init__(self, esquerda: ExpressaoConstrutor, operador: str, direita: ExpressaoConstrutor):
        super().__init__("Binário")
        self.esquerda = esquerda
        self.operador = operador
        self.direita = direita

class Numero(ExpressaoConstrutor):
    def __init__(self, valor: str):
        super().__init__("Número")
        self.valor = valor

class Variavel(ExpressaoConstrutor):
    def __init__(self, nome: str):
        super().__init__("Variável")
        self.nome = nome

class Atribuicao(ExpressaoConstrutor):
    def __init__(self, nome: str, expressao: ExpressaoConstrutor):
        super().__init__("Atribuição")
        self.nome = nome
        self.expressao = expressao
        variaveis_salvas[nome] = expressao

class Parenteses(ExpressaoConstrutor):
    def __init__(self, expressao: ExpressaoConstrutor):
        super().__init__("Parênteses")
        self.expressao = expressao

class Funcoes(ExpressaoConstrutor):
    def __init__(self, nome: str, expressao: list):
        super().__init__("Função")
        self.nome = "sqrt"
        self.expressao = expressao

class ExpVazia(ExpressaoConstrutor):
    def __init__(self):
        super().__init__("Vazia")



variaveis_salvas: dict = {}

class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.indice = 0
        self.proximo_token = tokens[self.indice]
        
    def espiadinha(self, tag: str):
        return self.proximo_token.tag == tag
    
    def consome(self, tag: str):
        if self.espiadinha(tag):
            self.indice += 1
            self.proximo_token = self.tokens[self.indice]
            return self.tokens[self.indice - 1]
        else:
            raise SyntaxError('Contra a gramática: Errou a sintax em algum lugar. \n Não implementamos a contagem de linhas e colunas. Somos bobões!')
    
    def parserVS(self):
        e = ExpVazia()

        while True:
            if self.espiadinha("FIM"):
                return e
            elif self.espiadinha("VARIÁVEL"):
                var = self.consome("VARIÁVEL")
                self.consome("ATRIBUIÇÃO")
                exp = self.parserE()
                e = Atribuicao(var.valor, exp)
                if not self.espiadinha("LINHA"):
                    if self.espiadinha("FIM"):
                        return e
                    raise SyntaxError('Contra a gramática: Esqueceu de pular linha. Tu é bobão!')
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
                    raise SyntaxError('Contra a gramática: Esqueceu de pular linha. Tu é bobão!')
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
            raise SyntaxError('Contra a gramática: Não mandou nem imprimir nem declarou variável.')

    def parserE(self):
        e = self.parserT()
        while True:
            if self.espiadinha("FIM"):
                return e
            elif self.espiadinha("SOMA"):
                self.consome("SOMA")
                e = OperadorBinario(e, "+", self.parserT())
            elif self.espiadinha("SUBTRAÇÃO"):
                self.consome("SUBTRAÇÃO")
                e = OperadorBinario(e, "-", self.parserT())
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
                e = OperadorBinario(e, "*", self.parserF())
            elif self.espiadinha("DIVISÃO"):
                self.consome("DIVISÃO")
                e = OperadorBinario(e, "/", self.parserF())
            else:
                break
        return e
    
    def parserF(self):
        if self.espiadinha("NÚMERO"):
            n = self.consome("NÚMERO")
            return Numero(float(n.valor))
        
        elif self.espiadinha("VARIÁVEL"):
            v = self.consome("VARIÁVEL")
            return Variavel(v.valor)
                        
        elif self.espiadinha("ABRE"):
            self.consome("ABRE")
            e = self.parserE()
            self.consome("FECHA")
            return Parenteses(e)
            
        elif self.espiadinha("SUBTRAÇÃO"):
            self.consome("SUBTRAÇÃO")
            e = self.parserF()
            return OperadorUnario("-", e)
        
        elif self.espiadinha("RAIZ"):
            function = self.consome("RAIZ").valor
            if self.espiadinha("ABRE"):
                self.consome("ABRE")
                e = self.parserE()
                self.consome("FECHA")
                return Funcoes(function, [e])




contas = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
}

def calcula(expressao, variables: dict = variaveis_salvas):
    match expressao.tag:
        case 'Binário':
            return contas[expressao.operador](calcula(expressao.esquerda), calcula(expressao.direita))
        case "Número":
            return expressao.valor
        case "Unário":
            if expressao.operador == "-":
                return -calcula(expressao.expressao, variables)
            else:
                raise SyntaxError('Contra a gramática: A gramática só aceita o unário "-".')
        case "Variável":
            return calcula(variables[expressao.nome], variables)
        case "Parênteses":
            return calcula(expressao.expressao, variables)
        case "Função":
            return math.sqrt(calcula(expressao.expressao[0], variables))
        case "Vazia":
            return 0
        case "Atribuição":
            return calcula(expressao.expressao, variables) 
        case _:
            raise SyntaxError('Tipo inválido de Token.')

def expressao_string(expressao, variables: dict = variaveis_salvas):
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
            return "sqrt(" + ", ".join([expressao_string(valor, variables) for valor in expressao.expressao]) + ")"
        case "Vazia":
            return ""
        case "Atribuição":
            return expressao.nome + " = " + expressao_string(expressao.expressao, variables)
        case _:
            raise SyntaxError('Tipo inválido de Token.')
