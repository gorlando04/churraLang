import os
import subprocess
from bs4 import BeautifulSoup

def extrair_resumo(html_path):
    with open(html_path, encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    h1s = soup.find_all("h1")
    total = h1s[1].text.strip()  # Ex: Total do churrasco: R$xxx.xx
    tabela_principal = soup.find("table")
    linhas = tabela_principal.find_all("tr")[1:]

    pagamentos = []
    for linha in linhas:
        tds = linha.find_all("td")
        nome = tds[0].text.strip()
        deve = tds[3].text.strip().replace("R$", "").replace(",", ".")
        pagamentos.append(f"{nome} deve pagar: R${float(deve):.2f}")

    return f"{total}\n" + "\n".join(sorted(pagamentos))

def testar_todos():
    base_path = "casos-teste"
    falhas = 0
    for i in range(1, 12):
        entrada = os.path.join(base_path, f"teste{i}.churra")
        esperado = os.path.join(base_path, f"teste{i}.expected")

        print(f"\n🔎 Rodando teste {i}...")
        try:
            subprocess.run(["python", "main.py", entrada], check=True)
            gerado_txt = extrair_resumo("saida_churrasco.html")
            with open(esperado, encoding="utf-8") as f:
                esperado_txt = f.read().strip()

            if gerado_txt.strip() == esperado_txt.strip():
                print(f"✅ Teste {i} passou!")
            else:
                print(f"❌ Teste {i} FALHOU.")
                print("🔸 Esperado:\n" + esperado_txt)
                print("🔸 Gerado:\n" + gerado_txt)
                falhas += 1
        except Exception as e:
            print(f"❌ Erro ao rodar o teste {i}: {e}")
            falhas += 1

    print(f"\n📋 Resumo: {11 - falhas} testes passaram, {falhas} falharam.")

if __name__ == "__main__":
    testar_todos()