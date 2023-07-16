import re
# Interpretador léxico para expressões aritméticas e atribuições em python.
# Muitas das coisas aqui foram tiradas da documentação abaixo:
# https://docs.python.org/3.8/reference/lexical_analysis.html

# Autores:
# Lucas de Lyra Monteiro
# João David Jotta
# Pedro Poppolino



# Cada token é formado por um tipo (categoria) e um valor (encontrado no texto) 
class Token:
    def __init__(self, tag, valor):
        self.tag = tag
        self.valor = valor


# Função que define os tipos de token a serem identificados (tirando o EOF, que é adicionado no final)
def define_categorias():

    #INTEIROS
    nonzerodigit = r"[1-9]"
    digit = r"[0-9]"
    bindigit = r"[0-1]"
    octdigit = r"[0-7]"
    hexdigit = fr"{digit}|[a-f]|[A-F]"

    hexinteger = fr"(0(x|X)(_?{hexdigit})+)"
    octinteger = fr"(0(o|O)(_?{octdigit})+)"
    bininteger = fr"(0(b|B)(_?{bindigit})+)"
    decinteger = fr"(({nonzerodigit}(_?{digit})*)|0+(_?0)*)"
    integernumber = fr"{bininteger}|{octinteger}|{decinteger}|{hexinteger}" 


    #FLUTUANTES
    digitpart = fr"{digit}(_?{digit})*"
    fraction = fr"\.{digitpart}"
    exponent = fr"(e|E)(\+|\-){digitpart}"
    pointfloat = fr"(({digitpart})?{fraction})|({digitpart}\.)"
    exponentfloat = fr"({pointfloat}|{digitpart}){exponent}"
    floatnumber = fr"{exponentfloat}|{pointfloat}"

    #NOVA LINHA
    linhanova = r"(\r\n)|(\n\r)|(\r)|(\n)"

    categorias = {
        "RAIZ": re.compile(r"(math\.)?sqrt"),

        "VARIÁVEL": re.compile(r"[a-zA-Z_][a-zA-Z_0-9]*"),
        
        "NÚMERO": re.compile(fr"{floatnumber}|{integernumber}"),
        
        "ATRIBUIÇÃO": re.compile(r"="),

        "IMPRESSÃO": re.compile(r"@"), 

        "SOMA": re.compile(r"\+"),

        "SUBTRAÇÃO": re.compile(r"-"),

        "MULTIPLICAÇÃO": re.compile(r"\*"),

        "DIVISÃO": re.compile(r"/"),     

        "ABRE": re.compile(r"\("),

        "FECHA": re.compile(r"\)"),

        "ESPAÇO": re.compile(r" +"), 

        "LINHA": re.compile(fr"{linhanova}")
    }

    return categorias



# Função que identifica o token da vez e o retorna
def identifica_token(entrada, pos, categoria):
    
    for tipo in categoria:
        alvo = categoria[tipo].match(entrada, pos)
        
        if alvo is None:
            continue

        if tipo == "ESPAÇO":
            return alvo.end(), None 

        palavra = None

        if tipo == "VARIÁVEL" or tipo == "NÚMERO": 
            palavra = alvo.group(0)
        
        return alvo.end(), Token(tipo, palavra)

    return pos, None



# Identifica todos os tokens válidos do arquivo e retorna uma lista desses tokens
def analisador_lexico(arquivo):
    i = 0
    lista_tokens = []
    categoria = define_categorias()


    while i < len(arquivo):
        ant = i
        i, novo_token = identifica_token(arquivo, i, categoria) 

        if ant == i:
            print(fr'{arquivo[i]} não reconhecido por nenhum regex')
            i+=1
            continue

        if(novo_token != None):
            lista_tokens.append(novo_token)


    lista_tokens.append(Token("FIM", None))
    return lista_tokens
