# Analise de Vendas - Feira

Projeto Python para leitura, analise e visualizacao de dados de vendas a partir de uma planilha Excel.

## Estrutura correta

O codigo-fonte deve ficar concentrado dentro do pacote `analise_vendas/`. A raiz do projeto deve ter apenas arquivos de apoio, como `README.md`, ambiente virtual e arquivos ignorados.

```text
TesteTecnico-Driva/
├── README.md
└── analise_vendas/
    ├── __init__.py
    ├── __main__.py
    ├── config.py
    ├── dados.py
    ├── exportacao.py
    ├── formatacao.py
    └── visualizacoes.py
```

Arquivos gerados em execucao, como `__pycache__/`, `.DS_Store`, `output/` e PDFs exportados, nao fazem parte da estrutura do codigo.

## Requisitos

```bash
pip install pandas matplotlib seaborn openpyxl
```

## Uso via CLI

Execute sempre a partir da raiz do projeto:

```bash
# Basico - gera PNGs na pasta ./output
python -m analise_vendas dados.xlsx

# Diretorio de saida customizado
python -m analise_vendas dados.xlsx --output ./relatorios

# Multiplos formatos (PNG + PDF consolidado)
python -m analise_vendas dados.xlsx --formato png pdf

# Trocar produto do Desafio 3 e tamanho dos rankings
python -m analise_vendas dados.xlsx --produto Laranja --top 5
```

Se estiver rodando em ambiente sem interface grafica, use:

```bash
MPLBACKEND=Agg python -m analise_vendas dados.xlsx
```

## Uso como biblioteca

```python
from analise_vendas.config import aplicar_estilo
from analise_vendas.dados import carregar_dados
from analise_vendas.visualizacoes import evolucao_faturamento

aplicar_estilo()
df = carregar_dados("dados.xlsx")

fig = evolucao_faturamento(df)
fig.savefig("meu_grafico.png")
```

## Formato esperado do Excel

O arquivo deve conter duas abas:

- `produtos`: `ID_PRODUTO`, `NOME_PRODUTO`, `PRECO_KG` ou `PREÇO_KG`, `PESO_MEDIO_UNITARIO_KG`
- `vendas`: `DATA`, `ID_PRODUTO`, `VALOR_VENDA`, `FAIXA_HORARIO`

## Customizacao

Edite [analise_vendas/config.py](/Users/pedroszpak/workspace/TesteTecnico-Driva/analise_vendas/config.py) para alterar:

- `PALETA`: cores dos graficos
- `STYLE_CONFIG`: tamanhos, DPI e espacamento
- `DIAS_PT`: traducao dos dias da semana
