import ply.lex as lex


# Definição dos tokens. Nessa etapa a Gramática da linguagem é definida
tokens = (
    'AMIGO', 'CONTRIBUI', 'VEGETARIANO',
    'ITEM', 'PRECO_KG', 'PRECO_L', 'PRECO_UNIT',
    'CARNE', 'BEBIDA', 'COMIDA', 'ENTRETENIMENTO',
    'QUANTIDADE_KG', 'QUANTIDADE_L', 'QUANTIDADE',
    'RATEIO', 'IGUAL',
    'STRING', 'NUMERO',
)

t_AMIGO = r'amigo'
t_CONTRIBUI = r'contribui'
t_VEGETARIANO = r'vegetariano'
t_ITEM = r'item'
t_PRECO_KG = r'preco_kg'
t_PRECO_L = r'preco_L'
t_PRECO_UNIT = r'preco_unit'
t_CARNE = r'carne'
t_BEBIDA = r'bebida'
t_COMIDA = r'comida'
t_ENTRETENIMENTO = r'entretenimento'
t_QUANTIDADE_KG = r'quantidade_kg'
t_QUANTIDADE_L = r'quantidade_L'
t_QUANTIDADE = r'quantidade'
t_RATEIO = r'rateio'
t_IGUAL = r'igual'
t_STRING = r'"[^"]*"'


# Função para checar se o valor passado é um número
def t_NUMERO(t):
    r'-?\d+(\.\d+)?'
    t.value = float(t.value)
    return t

t_ignore = ' \t\r'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Função para gerar o erro e informar em qual linha aconteceu o erro
def t_error(t):
    split = '\n'
    raise SyntaxError(f"[LÉXICO] ERRO LEXICO '{str(t.value).split(split)[0]}' na linha {t.lineno}")

# Objeto para fazer o gerenciamento da parte léxica
lexer = lex.lex()