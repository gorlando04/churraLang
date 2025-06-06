import sys

sys.path.append('src')

from src.churralang_parser import parser, amigos, itens
from src.churralang_codegen import gerar_html


sys.path.append(".")


if len(sys.argv) != 2:
    print("Uso: python churralang_main.py <arquivo.churra>")
    exit(1)

arquivo = sys.argv[1]
with open(arquivo, encoding="utf-8") as f:
    codigo = f.read()

try:
    parser.parse(codigo)
    html = gerar_html(amigos, itens)
    with open("saida_churrasco.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ Arquivo 'saida_churrasco.html' gerado com sucesso.")
except Exception as e:
    print("❌ Erro:", e)