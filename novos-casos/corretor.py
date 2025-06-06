import sys
from bs4 import BeautifulSoup
import subprocess
import os


def extrair_resumo(html_path):
    with open(html_path, encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Captura o segundo <h1> que contém o total
    h1s = soup.find_all("h1")
    if len(h1s) < 2:
        raise ValueError("HTML não contém dois <h1> esperados")
    total = h1s[1].text.strip()

    # Primeira tabela com dados dos amigos
    tabela_principal = soup.find("table")
    if not tabela_principal:
        raise ValueError("Tabela principal de amigos não encontrada")

    linhas = tabela_principal.find_all("tr")[1:]

    pagamentos = []
    for linha in linhas:
        tds = linha.find_all("td")
        nome = tds[0].text.strip()
        deve = tds[3].text.strip().replace("R$", "").replace(",", ".")
        pagamentos.append(f"{nome} deve pagar: R${float(deve):.2f}")

    return f"{total}\n" + "\n".join(sorted(pagamentos))

def comparar(nome_arquivo):
    expected_path = f"novos-casos/{nome_arquivo.split('.')[0]}.expected"
    html_path = "saida_churrasco.html"
    entrada = os.path.join('novos-casos', nome_arquivo)

    print(f"🔎 Verificando teste {nome_arquivo}...\n")
    try:
        subprocess.run(["python", "main.py", entrada], check=True)
        gerado_txt = extrair_resumo(html_path)

        with open(expected_path, encoding="utf-8") as f:
            esperado_txt = f.read().strip()

        if gerado_txt.strip() == esperado_txt.strip():
            print("✅ Teste passou! Saída igual à esperada.")
        else:
            print("❌ Teste falhou.")
            print("\n🔸 Esperado:")
            print(esperado_txt)
            print("\n🔸 Gerado:")
            print(gerado_txt)
    except Exception as e:
        print(f"❌ Erro ao processar o teste {nome_arquivo}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Uso: python novos-casos/corretor.py <nome-arquivo>.churra")
        sys.exit(1)
    comparar(sys.argv[1])