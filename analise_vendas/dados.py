"""
Leitura, merge e preparacao do DataFrame de vendas.
"""

import sys
import unicodedata
from pathlib import Path

import pandas as pd


def _normalizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    mapeamento = {}
    for coluna in df.columns:
        coluna_normalizada = unicodedata.normalize("NFKD", str(coluna))
        coluna_normalizada = coluna_normalizada.encode("ascii", "ignore").decode("ascii")
        coluna_normalizada = coluna_normalizada.replace(" ", "_").upper()
        mapeamento[coluna] = coluna_normalizada
    return df.rename(columns=mapeamento)


def carregar_dados(caminho: str) -> pd.DataFrame:
    caminho = Path(caminho)
    if not caminho.exists():
        print(f"[ERRO] Arquivo nao encontrado: {caminho}")
        sys.exit(1)

    vendas = _normalizar_colunas(pd.read_excel(caminho, sheet_name="vendas"))
    produtos = _normalizar_colunas(pd.read_excel(caminho, sheet_name="produtos"))

    df = vendas.merge(produtos, on="ID_PRODUTO", how="left")
    df["DATA"] = pd.to_datetime(df["DATA"])
    df["DIA_SEMANA"] = df["DATA"].dt.day_name()
    df["MES"] = df["DATA"].dt.to_period("M")
    df["QTD_KG"] = df["VALOR_VENDA"] / df["PRECO_KG"]

    orfaos = df["NOME_PRODUTO"].isna().sum()
    if orfaos > 0:
        print(f"[AVISO] {orfaos} registros de venda sem produto correspondente.")

    return df


def resumo_dados(df: pd.DataFrame):
    print("\n" + "=" * 60)
    print("RESUMO DA BASE")
    print("=" * 60)
    print(
        f"  Periodo........: {df['DATA'].min().strftime('%d/%m/%Y')} "
        f"a {df['DATA'].max().strftime('%d/%m/%Y')}"
    )
    print(f"  Registros......: {len(df):,}")
    print(f"  Produtos.......: {df['NOME_PRODUTO'].nunique()}")
    print(f"  Faturamento....: R$ {df['VALOR_VENDA'].sum():,.2f}")
    print("=" * 60)
