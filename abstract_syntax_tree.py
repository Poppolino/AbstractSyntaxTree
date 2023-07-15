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
        self.tag = "Variable"

class ExpConstParenteses:
    def __init__(self, expressao):
        self.expressao = expressao
        self.tag = "Parênteses"

class ExpConstFuncoes:
    def __init__(self, nome: str, expressao: list):
        self.nome = nome
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
    
    def parseVS(self):
        e = ExpVazia()

        while True:
            if self.espiadinha("EOF"):
                return e
            elif self.espiadinha("VARIABLE"):
                var = self.consome("VARIABLE")
                self.consome("EQUAL")
                exp = self.parseE()
                e = ExpConstAtribuicao(var.valor, exp)
                if not self.espiadinha("NEWLINE"):
                    if self.espiadinha("EOF"):
                        return e
                    raise SyntaxError('Tu é bobão!')
            else:
                break
        return e
        
    def parsePS(self):
        e = ExpVazia()

        while True:
            if self.espiadinha("EOF"):
                return e
            elif self.espiadinha("PRINT"):
                self.consome("PRINT")
                e = self.parseE()
                if not self.espiadinha("NEWLINE"):
                    if self.espiadinha("EOF"):
                        return e
                    raise SyntaxError('Tu é bobão!')
            else:
                break
        return e

    def parseS(self):
        if self.espiadinha("VARIABLE"):
            return self.parseVS()
        elif self.espiadinha("PRINT"):
            return self.parsePS()
        elif self.espiadinha("NEWLINE") or self.espiadinha("EOF"):
            return ExpVazia()
        else:
            raise SyntaxError('Tu é bobão!')

    def parseE(self):
        e = self.parseT()
        while True:
            if self.espiadinha("EOF"):
                return e
            elif self.espiadinha("SUM"):
                self.consome("SUM")
                e = ExpConstOperadorBinario(e, "+", self.parseT())
            elif self.espiadinha("SUB"):
                self.consome("SUB")
                e = ExpConstOperadorBinario(e, "-", self.parseT())
            else:
                break
        return e
    
    def parseT(self):
        e = self.parseF()
        while True:
            if self.espiadinha("EOF"):
                return e
            elif self.espiadinha("MULT"):
                self.consome("MULT")
                e = ExpConstOperadorBinario(e, "*", self.parseF())
            elif self.espiadinha("DIV"):
                self.consome("DIV")
                e = ExpConstOperadorBinario(e, "/", self.parseF())
            else:
                break
        return e
    
    def parseF(self):
        if self.espiadinha("NUM"):
            n = self.consome("NUM")
            return ExpConstNumero(int(n.valor))
        
        elif self.espiadinha("VARIABLE"):
            v = self.consome("VARIABLE")
            return ExpConstVariavel(v.valor)
                        
        elif self.espiadinha("PARENTESES_L"):
            self.consome("PARENTESES_L")
            e = self.parseE()
            self.consome("PARENTESES_R")
            return ExpConstParenteses(e)
            
        elif self.espiadinha("SUB"):
            self.consome("SUB")
            e = self.parseF()
            return ExpConstOperadorUnario("-", e)
        
        elif self.espiadinha("FUNCTION"):
            function = self.consome("FUNCTION").valor
            if self.espiadinha("PARENTESES_L"):
                self.consome("PARENTESES_L")
                e = self.parseE()
                self.consome("PARENTESES_R")
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
        case "Variable":
            return avaliar(variables[expressao.nome], variables)
        case "Parênteses":
            return avaliar(expressao.expressao, variables)
        case "Função":
            match expressao.nome:                
                case "sin":
                    return math.sin(avaliar(expressao.expressao[0], variables))
                case "cos":
                    return math.cos(avaliar(expressao.expressao[0], variables))
                case "sqrt":
                    if avaliar(expressao.expressao[0], variables) < 0:
                        raise ValueError("Square root of negative Número")
                    return math.sqrt(avaliar(expressao.expressao[0], variables))
                case _:
                    raise SyntaxError('Tu é bobão!')
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
        case "Variable":
            return expressao_string(variables[expressao.nome], variables)
        case "Parênteses":
            return "(" + expressao_string(expressao.expressao, variables) + ")"
        case "Função":
            return expressao.nome + "(" + ", ".join([expressao_string(argument, variables) for argument in expressao.expressao]) + ")"
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
        case "Variable":
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