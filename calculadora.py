from sys import stdin
from lexer import *
from abstract_syntax_tree import *

def interpreta_linhas(lista_tokens: list):
    tokens_por_linha = []
    aux = []
    for indice, token in enumerate(lista_tokens):
        #print(token.valor)
        aux.append(token)
        if token.tag == "LINHA":
            tokens_por_linha.append(aux)
            aux = []
        elif indice == len(lista_tokens)-1:
            tokens_por_linha.append(aux)
    return tokens_por_linha

if __name__ == '__main__':
    arquivo = stdin.read()
    
    inicio = fim = 0
    lista_tokens = analisador_lexico(arquivo)
    tokens_por_linha = interpreta_linhas(lista_tokens)
    
    impressao = 1
    for token in tokens_por_linha:
        parser = Parser(token).parserS()
        if token[0].tag == "IMPRESSÃO":
            
            inicio = arquivo.find('@', inicio)+1
            fim = arquivo.find('\n', inicio)
            
            print(f"\n{impressao}ª impressão a ser interpretada é: {arquivo[inicio:fim].strip()}")
            print(f"Considerando as variaveis dadas temos: {expressao_string(parser)}")
            print(f"Portanto, o resultado é: {avaliar(parser)}\n")
            
            impressao += 1





## 2º Etapa: Gera as árvores de expressões aritméticas e um dicionário com o valor das variáveis
## 3º Etapa: Calcula e apresenta o resultado das expressões com base nos valores das variáveis