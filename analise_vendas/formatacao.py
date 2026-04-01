"""
Funcoes auxiliares para formatacao de valores e rotulacao de graficos.
"""


def fmt_reais(x, _=None):
    return f"R$ {x:,.0f}"


def fmt_reais_dec(v):
    return f"R$ {v:,.2f}"


def rotular_barras_h(ax, valores, fontsize=11):
    margem = max(valores) * 0.01 if valores else 0
    for i, v in enumerate(valores):
        ax.text(
            v + margem,
            i,
            fmt_reais_dec(v),
            va="center",
            fontsize=fontsize,
            fontweight="bold",
        )


def rotular_barras_v(ax, barras, fontsize=10, offset=300):
    for barra in barras:
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height() + offset,
            fmt_reais(barra.get_height()),
            ha="center",
            fontsize=fontsize,
            fontweight="bold",
        )
