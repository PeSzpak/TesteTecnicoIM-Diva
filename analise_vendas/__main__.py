"""
Ponto de entrada via CLI.

Uso:
    python -m analise_vendas dados.xlsx
    python -m analise_vendas dados.xlsx --output ./relatorios
    python -m analise_vendas dados.xlsx --formato png pdf
    python -m analise_vendas dados.xlsx --produto Laranja --top 5
"""

import argparse
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

from .config import aplicar_estilo
from .dados import carregar_dados, resumo_dados
from .exportacao import salvar_figura, salvar_pdf_consolidado
from .visualizacoes import (
    estrategias,
    evolucao_faturamento,
    melhor_dia,
    quantidade_kg,
    vendas_produto,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analise de Vendas - Feira",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python -m analise_vendas dados.xlsx
  python -m analise_vendas dados.xlsx -o ./relatorios
  python -m analise_vendas dados.xlsx -f png pdf svg
  python -m analise_vendas dados.xlsx -p Laranja -t 5
        """,
    )
    parser.add_argument("arquivo", help="Caminho do arquivo Excel (.xlsx)")
    parser.add_argument(
        "--output",
        "-o",
        default="./output",
        help="Diretorio de saida (padrao: ./output)",
    )
    parser.add_argument(
        "--formato",
        "-f",
        nargs="+",
        default=["png"],
        choices=["png", "pdf", "svg", "jpg"],
        help="Formatos de saida (padrao: png)",
    )
    parser.add_argument(
        "--produto",
        "-p",
        default="Banana",
        help="Produto para o Desafio 3 (padrao: Banana)",
    )
    parser.add_argument(
        "--top",
        "-t",
        type=int,
        default=10,
        help="Quantidade de itens nos rankings (padrao: 10)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    aplicar_estilo()

    print(f"\n{'=' * 60}")
    print(f"  ANALISE DE VENDAS - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"  Arquivo: {args.arquivo}")
    print(f"  Saida..: {output_dir.resolve()}")
    print(f"{'=' * 60}")

    df = carregar_dados(args.arquivo)
    resumo_dados(df)

    figuras = {}
    print("\n--- Gerando visualizacoes ---")

    fig1 = evolucao_faturamento(df)
    salvar_figura(fig1, output_dir, "desafio1_evolucao_faturamento", args.formato)
    figuras["desafio1"] = fig1

    fig2 = melhor_dia(df, top_n=args.top)
    salvar_figura(fig2, output_dir, "desafio2_melhor_dia", args.formato)
    figuras["desafio2"] = fig2

    fig3 = vendas_produto(df, produto=args.produto, top_n=args.top)
    salvar_figura(fig3, output_dir, f"desafio3_{args.produto.lower()}", args.formato)
    figuras["desafio3"] = fig3

    fig4 = quantidade_kg(df)
    salvar_figura(fig4, output_dir, "desafio4_quantidade_kg", args.formato)
    figuras["desafio4"] = fig4

    fig5 = estrategias(df)
    salvar_figura(fig5, output_dir, "desafio5_estrategias", args.formato)
    figuras["desafio5"] = fig5

    if "pdf" in args.formato:
        salvar_pdf_consolidado(figuras, output_dir)

    plt.close("all")

    print(f"\n{'=' * 60}")
    print("  Analise concluida com sucesso!")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
