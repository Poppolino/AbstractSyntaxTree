from sys import stdin
from lexer import *


arquivo = stdin.read()
lista_tokens = analisador_lexico(arquivo) 
## 2º Etapa: Gera as árvores de expressões aritméticas e um dicionário com o valor das variáveis
## 3º Etapa: Calcula e apresenta o resultado das expressões com base nos valores das variáveis