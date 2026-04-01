"""
Funcoes de exportacao: salvar figuras individuais e PDF consolidado.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def salvar_figura(fig: plt.Figure, caminho: Path, nome: str, formatos: list):
    for fmt in formatos:
        if fmt == "pdf":
            continue
        arquivo = caminho / f"{nome}.{fmt}"
        fig.savefig(arquivo)
        print(f"  -> {arquivo}")


def salvar_pdf_consolidado(figuras: dict, caminho: Path):
    arquivo = caminho / "relatorio_completo.pdf"
    with PdfPages(arquivo) as pdf:
        for fig in figuras.values():
            pdf.savefig(fig)
    print(f"\n  -> PDF consolidado: {arquivo}")
