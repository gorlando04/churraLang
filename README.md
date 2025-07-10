# 🥩 ChurraLang

**ChurraLang** é uma linguagem declarativa desenvolvida para o T6 da disciplina de compiladores. Seu objetivo é realizar o rateio justo do custo de um churrasco entre amigos, gerando uma saída HTML estruturada.

## Desenvolvido por: Gabriel Orlando. RA: 790728 

Vídeo curto demonstrando as funcionalidades da linguagem: [Link do video](https://youtu.be/fBAdz9tfYzg)

## Objetivo do projeto

- Criar uma linguagem específica com análise léxica, sintática e semântica
- Permitir descrição declarativa de:
  - Participantes (vegetarianos ou não)
  - Itens consumidos (carne, bebida, comida, entretenimento)
- Calcular:
  - Quanto cada um deve pagar
  - Transferências justas entre amigos
- Gerar um **HTML final com todas as informações do churrasco**

---

## Estrutura do projeto

```
└── src/
├── churralang_lexer.py         # Analisador léxico (tokens)
├── churralang_parser.py        # Parser + verificações semânticas
├── churralang_codegen.py       # Geração do HTML final

└──main.py          # Entrada principal do compilador

└── casos-teste/ # Casos de teste para validação
│   ├── teste1.churra
│   ├── teste1.expected
│   ├── …
│   ├── corretor.py

└── casos-teste-lexica/ # Casos de teste de erros léxicos
│   ├── teste1.churra
│   ├── teste1.expected
│   ├── …

└── casos-teste-semantica/ # Casos de teste de erros semanticos
│   ├── teste1.churra
│   ├── teste1.expected
│   ├── …

└── casos-teste-sintatica/ # Casos de teste de erros sintáticos
│   ├── teste1.churra
│   ├── teste1.expected
│   ├── …

└── novos-casos/ # Pasta para inserir casos de teste novos com um corretor
│   ├── corretor.py
│   ├── teste1.churra
│   ├── teste1.expected

└── README.md                   # Este arquivo
```

---

## Tecnologias utilizadas

- **Python 3**
- **PLY (Python Lex-Yacc)** — Gerador de parser (léxico e sintático)
- **BeautifulSoup4** — Para leitura e correção de HTML

---

## Etapas do Compilador

### 1. Análise léxica (`churralang_lexer.py`)

Define os **tokens da linguagem**, como:
- Palavras-chave: `amigo`, `contribui`, `item`, `preco_kg`, `quantidade_kg`, `vegetariano`, `rateio`
- Strings (`"Andre"`)
- Números positivos e negativos (`-5`, `120.50`)

Utiliza **expressões regulares (regex)** para reconhecer os padrões.

---

### 2. Análise sintática (`churralang_parser.py`)

Define a **gramática** da linguagem com PLY (yacc).
Exemplo de produção:

```yacc
declaracao_amigo : AMIGO STRING CONTRIBUI NUMERO vegetariano_opt
```

Garante que comandos estejam bem formados, com ordem e estruturas corretas.

### 3. Análise semântica

São feitas durante o parsing, com verificações adicionais:



	•	✅ Verificação 1 – O total investido por todos os amigos deve ser ≥ custo total do churrasco
	•	✅ Verificação 2 – Carnes só podem existir se houver ao menos um não vegetariano
	•	✅ Verificação 3 – Nomes de carnes não podem se repetir
	•	✅ Verificação 4 – Não podemos ter preço negativo ou quantidade não positiva
	•	✅ Verificação 5 – Não pode haver nomes repetidos de amigos
	•	✅ Verificação 6 – Não podemos ter mais de um item de entrenimento

### 4. Geração de código (churralang_codegen.py)

Cria um HTML com:

	•	Tabela com:
		•	Nome
		•	Status (vegetariano ou não)
		•	Quanto contribuiu
		•	Quanto deve pagar
		•	Saldo
	•	Cálculo de transferências entre participantes
	•	Lista de itens consumidos com tipo, nome, preço, quantidade e total

### 5. Tratamento de erros

Mensagens claras para erros como:

	•	Token inválido
	•	Sintaxe incorreta
	•	Regras semânticas violadas (ex: carne sem carnívoros)
	•	Nome de carne repetido

Os erros são lançados com mensagens explicativas e encerram a compilação com sys.exit(1).

Abaixo podemos ver exemplos de erros:

**Léxicos**:

```text
amig "Felipe" contribui 100
amigo "João" contribui 100
amigo "Mariana" contribui 100

item carne "picanha" preco_kg 60 quantidade_kg 3
item bebida preco_L 10 quantidade_L 6
item comida preco_unit 25 quantidade 2

rateio igual
```

Resultando em:

```text
❌ Erro: [LÉXICO] ERRO LEXICO 'amig "Felipe" contribui 100' na linha 1
```
---


**Sintáticos**:

```text
amigo "Felipe"  100
amigo "João" contribui 100
amigo "Mariana" contribui 100

item carne "picanha" preco_kg 60 quantidade_kg 3
item bebida preco_L 10 quantidade_L 6
item comida preco_unit 25 quantidade 2

rateio igual
```

Resultando em:

```text
❌ Erro: [SINTÁTICO] Erro de sintaxe na linha 1: token '100.0' inesperado
```
---

**Semânticos**:

```text
amigo "Felipe" contribui 100 vegetariano
amigo "João" contribui 100 vegetariano
amigo "Mariana" contribui 100 vegetariano

item carne "picanha" preco_kg 60 quantidade_kg 3
item bebida preco_L 10 quantidade_L 6
item comida preco_unit 25 quantidade 2

rateio igual
```

Resultando em:

```text
❌ Erro: [SEMÂNTICO] Nenhum amigo consome carne, mas há carnes declaradas.
```
---

### 6. Casos de Teste

Localizados na pasta casos-teste/, cada caso possui:
	•	Um arquivo .churra
	•	Um arquivo .expected com a saída textual esperada

Total de 11 casos cobrindo:

- ✅ Teste 1 – Rateio de comida simples

- ✅ Teste 2 – Rateio de bebida

- ✅ Teste 3 – Com vegetariano e carne

- ✅ Teste 4 – Rateio só de carne

- ✅ Teste 5 – Entretenimento e vegetariano

- ✅ Teste 6 – Múltiplas carnes

- ✅ Teste 7 – Vegetarianos não pagam carne

- ✅ Teste 8 – Comida + entretenimento

- ✅ Teste 9 – Bebida e comida baratas

- ✅ Teste 10 – Três pessoas, uma vegetariana

- ✅ Teste 11 – Muitas informações

Para realizar o teste dos casos de teste pode-se utilizar o seguinte comando:

```shell
python3 casos-teste/corretor.py
```

#### Criação de casos de teste

É possível criar caso de teste individuais para testar a amplitude do compilador. Para isso deve-se criar um arquivo **.churra** e um arquivo **.expected** que deve ter a saída esperada, semelhante às que existem na pasta [casos-teste](casos-teste/). Após isso para fazer a correção basta executar:

```shell
python novos-casos/corretor.py <nome-arquivo>.churra
```

#### 🚀 Como rodar o compilador

1.	Crie um arquivo .churra com as definições
2.	Execute:

```shell
python main.py <nome-arquivo>.churra
```
3.	O HTML será gerado como saida_churrasco.html



### 7. Dependências

Para conseguir rodar o compilador basta utilizar o arquivo requirements.txt.

```shell
pip install -r requirements.txt
```

### 8. Extra

Caso queira algo mais individual e esteja usando o sistema operacional baseado em Unix, você pode criar um alias para o compilador dessa maneira:

1. Abra o arquivo .bashrc localizado na sua pasta principal
2. alias churralang="python main.py"
3. Feche e abra o terminal
4. Execute:

```
churralang casos-teste/teste11.churra
```



### 9. Contribuições

Contribuições são bem-vindas! Aqui estão algumas formas de colaborar com o projeto:

🧠 Novas funcionalidades sugeridas

	•	Suporte a rateios personalizados (por porcentagem ou valor fixo)
	•	Inclusão de alergias ou restrições alimentares
	•	Exportação para PDF além de HTML
	•	Interface gráfica simples (GUI ou web)

🧪 Mais testes

	•	Criação de novos casos de teste com variações complexas
	•	Testes com erros propositalmente inseridos para validar mensagens de erro

🧹 Refatoração e melhorias

	•	Modularização mais fina do código
	•	Separação dos dados e lógica de apresentação
	•	Validações adicionais no parser

🛠 Como contribuir

1.	Faça um fork do projeto
2.	Crie uma branch para sua feature:

```
git checkout -b minha-feature
```

3.	Faça commits claros:

```
git commit -m "Adiciona verificação de carne duplicada"
```

4.	Envie um pull request!





