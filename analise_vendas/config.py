"""
Configuracoes globais: paleta de cores, estilo dos graficos e constantes.
"""

import matplotlib.pyplot as plt
import seaborn as sns


PALETA = {
    "primaria": "#2563EB",
    "destaque": "#DC2626",
    "secundaria": "#F59E0B",
    "sucesso": "#10B981",
    "roxo": "#8B5CF6",
    "meses": [
        "#3B82F6",
        "#F59E0B",
        "#10B981",
        "#EF4444",
        "#8B5CF6",
        "#EC4899",
        "#14B8A6",
        "#F97316",
        "#6366F1",
        "#84CC16",
    ],
}

DIAS_PT = {
    "Monday": "Seg",
    "Tuesday": "Ter",
    "Wednesday": "Qua",
    "Thursday": "Qui",
    "Friday": "Sex",
    "Saturday": "Sab",
    "Sunday": "Dom",
}
DIAS_ORDEM = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

STYLE_CONFIG = {
    "figure.figsize": (14, 6),
    "font.size": 12,
    "axes.titlesize": 16,
    "axes.titleweight": "bold",
    "axes.labelsize": 13,
    "figure.dpi": 150,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.3,
}


def aplicar_estilo():
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update(STYLE_CONFIG)
