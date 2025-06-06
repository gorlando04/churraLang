def gerar_html(amigos, itens):
    carne_dict = itens.get('carne', {})
    carne = sum(c['total'] for c in carne_dict.values())
    bebida = itens.get('bebida', {'total': 0})['total']
    comida = itens.get('comida', {'total': 0})['total']
    entretenimento = itens.get('entretenimento', {'total': 0})['total']

    vegetarianos = [a for a, v in amigos.items() if v['vegetariano']]
    nao_vegetarianos = [a for a in amigos if not amigos[a]['vegetariano']]

    custo_carne = carne / len(nao_vegetarianos) if nao_vegetarianos else 0
    custo_restante = (bebida + comida + entretenimento) / len(amigos)

    total_geral = carne + bebida + comida + entretenimento
    saldos = {}

    total_investido = 0.0
    for nome in amigos:
        total_investido += amigos[nome]['contribuicao']

    add_html = ''

    if total_investido > total_geral:
        add_html = f'\n<h2>Investimento Total: {total_investido:.2f}, logo R$ {(total_investido-total_geral):.2f} foram investidos à mais</h2>'


    html = f"""<html><head><title>Churrasco</title></head><body>
    <h1>Divisão do churrasco</h1>
    <h1>Total do churrasco:</b> R${total_geral:.2f}</h1>{add_html}
    <table border="1"><tr><th>Amigo</th><th>Vegetariano</th><th>Contribuiu</th><th>Deve pagar</th><th>Saldo</th></tr>"""

    for nome in amigos:
        contrib = amigos[nome]['contribuicao']
        total_devido = custo_restante
        if not amigos[nome]['vegetariano']:
            total_devido += custo_carne
        saldo = round(contrib - total_devido, 2)
        saldos[nome] = saldo
        html += f"<tr><td>{nome}</td><td>{'Sim' if amigos[nome]['vegetariano'] else 'Não'}</td><td>R${contrib:.2f}</td><td>R${total_devido:.2f}</td><td>R${saldo:.2f}</td></td></tr>"

    html += f"</table>"

    # Transferências
    devedores = {k: -v for k, v in saldos.items() if v < 0}
    credores = {k: v for k, v in saldos.items() if v > 0}
    pagamentos = []

    for devedor in devedores:
        valor_a_pagar = devedores[devedor]
        for credor in list(credores.keys()):
            valor_a_receber = credores[credor]
            if valor_a_pagar <= 0 or valor_a_receber <= 0:
                continue
            valor = min(valor_a_pagar, valor_a_receber)
            pagamentos.append((devedor, credor, valor))
            devedores[devedor] -= valor
            credores[credor] -= valor
            valor_a_pagar -= valor

    html += "<h2>Transferências</h2><table border='1'><tr><th>Pagador</th><th>Recebedor</th><th>Valor</th></tr>"
    for pagador, recebedor, valor in pagamentos:
        html += f"<tr><td>{pagador}</td><td>{recebedor}</td><td>R${valor:.2f}</td></tr>"
    html += "</table>"

    # Lista final de itens
    html += "<h2>Itens consumidos</h2><table border='1'><tr><th>Tipo</th><th>Nome</th><th>Preço</th><th>Qtd</th><th>Total</th></tr>"
    for nome, info in carne_dict.items():
        html += f"<tr><td>carne</td><td>{nome}</td><td>R${info['preco']:.2f}</td><td>{info['qtd']}</td><td>R${info['total']:.2f}</td></tr>"
    for nome in ['bebida', 'comida', 'entretenimento']:
        if nome in itens:
            i = itens[nome]
            html += f"<tr><td>{i['tipo']}</td><td>{nome}</td><td>R${i['preco']:.2f}</td><td>{i['qtd']}</td><td>R${i['total']:.2f}</td></tr>"
    html += "</table></body></html>"

    return html