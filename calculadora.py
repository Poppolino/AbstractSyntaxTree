from sys import stdin
from lexer import *
from abstract_syntax_tree import *

def interpreta_linhas(lista_tokens: list):
    tokens_por_linha = []
    aux = []

    for indice, token in enumerate(lista_tokens):
        aux.append(token)
        
        if token.tag == "LINHA":
            tokens_por_linha.append(aux)
            aux = []
        elif indice == len(lista_tokens)-1:
            tokens_por_linha.append(aux)
    
    return tokens_por_linha


# Realiza a análise léxica, sintática e calcula o resultado das expressões
if __name__ == '__main__':
    inicio = fim = 0
    impressao = 1
    
    arquivo = stdin.read()

    lista_tokens = analisador_lexico(arquivo)
    tokens_por_linha = interpreta_linhas(lista_tokens)
    
    
    for token in tokens_por_linha:
        parser = Parser(token).parserS()
        if token[0].tag == "IMPRESSÃO":
            
            inicio = arquivo.find('@', inicio) + 1
            fim = arquivo.find('\n', inicio) if arquivo.find('\n', inicio) != -1 else None
            
            print(f"\n{impressao}ª impressão a ser interpretada é: {arquivo[inicio:fim].strip()}")
            print(f"Considerando as variaveis dadas temos: {expressao_string(parser)}")
            print(f"Portanto, o resultado é: {calcula(parser)}\n")
            
            impressao += 1