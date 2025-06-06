import ply.yacc as yacc
from churralang_lexer import tokens

# Dicionários para gerenciamento das informações
amigos = {}
itens = {}
modo_rateio = None


# Análise semantica da linguagem para checagem
def p_program(p):
    '''program : comandos'''
    total_contribuido = sum(info['contribuicao'] for info in amigos.values())
    total_churrasco = 0
    if 'carne' in itens:
        total_churrasco += sum(i['total'] for i in itens['carne'].values())
    for nome in ['bebida', 'comida', 'entretenimento']:
        if nome in itens:
            total_churrasco += itens[nome]['total']
    if round(total_contribuido, 2) < round(total_churrasco, 2):
        raise ValueError(f"[SEMÂNTICO] Total contribuído (R${total_contribuido:.2f}) é menor que o custo do churrasco (R${total_churrasco:.2f})")
    
    if 'carne' in itens:
        nao_vegetarianos = [a for a in amigos if not amigos[a]['vegetariano']]
        if not nao_vegetarianos:
            raise ValueError("[SEMÂNTICO] Nenhum amigo consome carne, mas há carnes declaradas.")
    p[0] = p[1]

def p_comandos(p):
    '''comandos : comandos comando
                | comando'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

def p_comando_amigo_normal(p):
    '''comando : AMIGO STRING CONTRIBUI NUMERO'''
    nome = p[2].strip('"')
    if nome in amigos:
        raise ValueError(f"[SEMÂNTICO] Amigo '{nome}' já foi definido")
    amigos[nome] = {'contribuicao': p[4], 'vegetariano': False}
    p[0] = ('amigo', nome)

def p_comando_amigo_veg(p):
    '''comando : AMIGO STRING CONTRIBUI NUMERO VEGETARIANO'''
    nome = p[2].strip('"')
    if nome in amigos:
        raise ValueError(f"[SEMÂNTICO] Amigo '{nome}' já foi definido")
    amigos[nome] = {'contribuicao': p[4], 'vegetariano': True}
    p[0] = ('amigo', nome)


def verify_preco_qtd(preco,qtd,name):
    if preco < 0:
        raise ValueError(f"[SEMÂNTICO] Preço {name} deve ser não-negativo.")
    if qtd <= 0:
        raise ValueError(f"[SEMÂNTICO] Quantidade {name} deve ser maior que zero")
    return

def p_comando_item_carne(p):
    '''comando : ITEM CARNE STRING PRECO_KG NUMERO QUANTIDADE_KG NUMERO'''
    nome = p[3].strip('"')
    preco, qtd = p[5], p[7]
    verify_preco_qtd(preco,qtd,'carne')
    if 'carne' not in itens:
        itens['carne'] = {}
    elif nome in itens['carne']:
        raise ValueError(f"[SEMÂNTICO] A carne '{nome}' já foi declarada anteriormente.")
    itens['carne'][nome] = {'tipo': 'carne', 'preco': preco, 'qtd': qtd, 'total': preco * qtd}

def p_comando_item_bebida(p):
    '''comando : ITEM BEBIDA PRECO_L NUMERO QUANTIDADE_L NUMERO'''
    preco, qtd = p[4], p[6]
    verify_preco_qtd(preco,qtd,'bebida')
    itens['bebida'] = {'tipo': 'bebida', 'preco': preco, 'qtd': qtd, 'total': preco * qtd}

def p_comando_item_comida(p):
    '''comando : ITEM COMIDA PRECO_UNIT NUMERO QUANTIDADE NUMERO'''
    preco, qtd = p[4], p[6]
    verify_preco_qtd(preco,qtd,'comida')
    itens['comida'] = {'tipo': 'comida', 'preco': preco, 'qtd': qtd, 'total': preco * qtd}

def p_comando_item_entretenimento(p):
    '''comando : ITEM ENTRETENIMENTO PRECO_UNIT NUMERO QUANTIDADE NUMERO'''
    preco, qtd = p[4], p[6]
    verify_preco_qtd(preco,qtd,'entrerimento')

    if qtd != 1:
        raise ValueError("[SEMÂNTICO] A quantidade de Entrenimento deve ser igual à 1")
    itens['entretenimento'] = {'tipo': 'entretenimento', 'preco': preco, 'qtd': qtd, 'total': preco * qtd}

def p_comando_rateio(p):
    '''comando : RATEIO IGUAL'''
    global modo_rateio
    modo_rateio = 'igual'
    p[0] = ('rateio', modo_rateio)

def p_error(p):
    if p:
        raise SyntaxError(f"[SINTÁTICO] Erro de sintaxe na linha {p.lineno}: token '{p.value}' inesperado")
    raise SyntaxError("[SINTÁTICO] Erro de sintaxe no final do arquivo")



parser = yacc.yacc()