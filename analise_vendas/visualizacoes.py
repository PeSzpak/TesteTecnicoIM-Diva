"""
Visualizacoes: um grafico por desafio.
"""

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import seaborn as sns

from .config import DIAS_ORDEM, DIAS_PT, PALETA
from .formatacao import fmt_reais, fmt_reais_dec, rotular_barras_h, rotular_barras_v


def evolucao_faturamento(df: pd.DataFrame) -> plt.Figure:
    fat_diario = df.groupby("DATA")["VALOR_VENDA"].sum().reset_index()
    fat_mensal = df.groupby("MES")["VALOR_VENDA"].sum().reset_index()
    fat_mensal["MES"] = fat_mensal["MES"].astype(str)

    fig, axes = plt.subplots(1, 2, figsize=(18, 6), gridspec_kw={"width_ratios": [2.5, 1]})

    ax = axes[0]
    ax.plot(
        fat_diario["DATA"],
        fat_diario["VALOR_VENDA"],
        color=PALETA["primaria"],
        linewidth=1.2,
        alpha=0.6,
    )
    mm7 = fat_diario["VALOR_VENDA"].rolling(7, center=True).mean()
    ax.plot(
        fat_diario["DATA"],
        mm7,
        color=PALETA["destaque"],
        linewidth=2.5,
        label="Media movel 7 dias",
    )
    ax.fill_between(
        fat_diario["DATA"],
        fat_diario["VALOR_VENDA"],
        alpha=0.07,
        color=PALETA["primaria"],
    )
    ax.set_title("Evolucao do Faturamento Diario")
    ax.set_xlabel("Data")
    ax.set_ylabel("Faturamento (R$)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_reais))
    ax.legend()
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

    ax2 = axes[1]
    cores = PALETA["meses"][: len(fat_mensal)]
    barras = ax2.bar(
        fat_mensal["MES"],
        fat_mensal["VALOR_VENDA"],
        color=cores,
        width=0.5,
        edgecolor="white",
    )
    rotular_barras_v(ax2, barras, offset=500, fontsize=11)
    ax2.set_title("Faturamento Mensal")
    ax2.set_ylabel("Faturamento (R$)")
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_reais))

    plt.tight_layout()

    variacao = (
        (fat_mensal.iloc[-1]["VALOR_VENDA"] - fat_mensal.iloc[0]["VALOR_VENDA"])
        / fat_mensal.iloc[0]["VALOR_VENDA"]
        * 100
    )
    print("\n[DESAFIO 1] Evolucao do Faturamento")
    print(f"  Faturamento total: {fmt_reais_dec(df['VALOR_VENDA'].sum())}")
    for _, row in fat_mensal.iterrows():
        print(f"  {row['MES']}: {fmt_reais_dec(row['VALOR_VENDA'])}")
    print(f"  Variacao primeiro->ultimo mes: {variacao:+.1f}%")

    return fig


def melhor_dia(df: pd.DataFrame, top_n: int = 10) -> plt.Figure:
    fat_dia = df.groupby("DATA")["VALOR_VENDA"].sum().reset_index()
    top = fat_dia.sort_values("VALOR_VENDA", ascending=False).head(top_n).reset_index(drop=True)
    top_inv = top.iloc[::-1].reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(14, 6))
    cores = [PALETA["primaria"]] * top_n
    cores[-1] = PALETA["destaque"]
    ax.barh(
        range(top_n),
        top_inv["VALOR_VENDA"],
        color=cores,
        edgecolor="white",
        height=0.6,
    )
    ax.set_yticks(range(top_n))
    ax.set_yticklabels(top_inv["DATA"].dt.strftime("%d/%m/%Y (%A)"))
    rotular_barras_h(ax, top_inv["VALOR_VENDA"].tolist())
    ax.set_title(f"Top {top_n} Melhores Dias em Vendas")
    ax.set_xlabel("Faturamento (R$)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_reais))
    plt.tight_layout()

    melhor = top.iloc[0]
    print(
        f"\n[DESAFIO 2] Melhor dia: {melhor['DATA'].strftime('%d/%m/%Y (%A)')}"
        f" - {fmt_reais_dec(melhor['VALOR_VENDA'])}"
    )

    return fig


def vendas_produto(df: pd.DataFrame, produto: str = "Banana", top_n: int = 10) -> plt.Figure:
    filtro = df[df["NOME_PRODUTO"] == produto]
    if filtro.empty:
        print(f"[AVISO] Produto '{produto}' nao encontrado na base.")
        return plt.figure()

    diario = filtro.groupby("DATA")["VALOR_VENDA"].sum().reset_index()
    top = diario.sort_values("VALOR_VENDA", ascending=False).head(top_n).reset_index(drop=True)
    top_inv = top.iloc[::-1].reset_index(drop=True)
    melhor = top.iloc[0]

    fig, axes = plt.subplots(1, 2, figsize=(18, 6), gridspec_kw={"width_ratios": [2, 1.2]})

    ax = axes[0]
    ax.plot(
        diario["DATA"],
        diario["VALOR_VENDA"],
        color=PALETA["secundaria"],
        linewidth=1.5,
        alpha=0.8,
    )
    ax.fill_between(
        diario["DATA"],
        diario["VALOR_VENDA"],
        alpha=0.12,
        color=PALETA["secundaria"],
    )
    ax.axvline(melhor["DATA"], color=PALETA["destaque"], linestyle="--", alpha=0.7)
    ax.annotate(
        f"Melhor dia\n{melhor['DATA'].strftime('%d/%m')}\n{fmt_reais_dec(melhor['VALOR_VENDA'])}",
        xy=(melhor["DATA"], melhor["VALOR_VENDA"]),
        xytext=(30, 20),
        textcoords="offset points",
        fontsize=10,
        fontweight="bold",
        color=PALETA["destaque"],
        arrowprops=dict(arrowstyle="->", color=PALETA["destaque"]),
    )
    ax.set_title(f"Vendas Diarias de {produto}")
    ax.set_xlabel("Data")
    ax.set_ylabel("Faturamento (R$)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_reais))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

    ax2 = axes[1]
    cores = [PALETA["secundaria"]] * top_n
    cores[-1] = PALETA["destaque"]
    ax2.barh(
        range(top_n),
        top_inv["VALOR_VENDA"],
        color=cores,
        edgecolor="white",
        height=0.6,
    )
    ax2.set_yticks(range(top_n))
    ax2.set_yticklabels(top_inv["DATA"].dt.strftime("%d/%m/%Y"))
    rotular_barras_h(ax2, top_inv["VALOR_VENDA"].tolist())
    ax2.set_title(f"Top {top_n} Dias - {produto}")
    ax2.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_reais))

    plt.tight_layout()

    print(
        f"\n[DESAFIO 3] Melhor dia de {produto}: "
        f"{melhor['DATA'].strftime('%d/%m/%Y (%A)')} - "
        f"{fmt_reais_dec(melhor['VALOR_VENDA'])}"
    )
    print(f"  Faturamento total de {produto}: {fmt_reais_dec(filtro['VALOR_VENDA'].sum())}")
    print(f"  N de vendas: {len(filtro):,}")

    return fig


def quantidade_kg(df: pd.DataFrame) -> plt.Figure:
    kg = df.groupby("NOME_PRODUTO")["QTD_KG"].sum().sort_values(ascending=True).reset_index()

    fig, ax = plt.subplots(figsize=(14, 7))
    cores = [PALETA["primaria"]] * len(kg)
    cores[-1] = PALETA["destaque"]
    ax.barh(range(len(kg)), kg["QTD_KG"], color=cores, edgecolor="white", height=0.6)
    ax.set_yticks(range(len(kg)))
    ax.set_yticklabels(kg["NOME_PRODUTO"])
    margem = kg["QTD_KG"].max() * 0.01
    for i, (_, row) in enumerate(kg.iterrows()):
        ax.text(
            row["QTD_KG"] + margem,
            i,
            f"{row['QTD_KG']:,.1f} kg",
            va="center",
            fontsize=11,
            fontweight="bold",
        )
    ax.set_title("Quantidade Vendida por Produto (kg)")
    ax.set_xlabel("Quantidade (kg)")
    plt.tight_layout()

    campeao = kg.iloc[-1]
    print(
        f"\n[DESAFIO 4] Produto mais vendido em kg: "
        f"{campeao['NOME_PRODUTO']} - {campeao['QTD_KG']:,.1f} kg"
    )
    print("  Ranking completo:")
    for posicao, (_, row) in enumerate(kg.iloc[::-1].iterrows(), 1):
        print(f"    {posicao:2d}. {row['NOME_PRODUTO']:<12} - {row['QTD_KG']:>10,.1f} kg")

    return fig


def estrategias(df: pd.DataFrame) -> plt.Figure:
    fat_diasem = df.groupby("DIA_SEMANA")["VALOR_VENDA"].sum().reindex(DIAS_ORDEM).reset_index()
    fat_horario = (
        df.groupby("FAIXA_HORARIO")["VALOR_VENDA"].sum().reset_index().sort_values("FAIXA_HORARIO")
    )
    ticket = (
        df.groupby("NOME_PRODUTO")
        .agg(
            FATURAMENTO=("VALOR_VENDA", "sum"),
            QTD_VENDAS=("VALOR_VENDA", "count"),
            TICKET_MEDIO=("VALOR_VENDA", "mean"),
        )
        .sort_values("FATURAMENTO", ascending=False)
        .reset_index()
    )
    pivot = df.pivot_table(
        values="VALOR_VENDA",
        index="FAIXA_HORARIO",
        columns="DIA_SEMANA",
        aggfunc="sum",
    )
    pivot = pivot.reindex(columns=DIAS_ORDEM)
    pivot.columns = [DIAS_PT.get(coluna, coluna) for coluna in pivot.columns]

    fig, axes = plt.subplots(2, 2, figsize=(18, 14))

    ax = axes[0, 0]
    dias_label = [DIAS_PT[dia] for dia in DIAS_ORDEM]
    cores = [PALETA["primaria"]] * 7
    cores[fat_diasem["VALOR_VENDA"].idxmax()] = PALETA["sucesso"]
    cores[fat_diasem["VALOR_VENDA"].idxmin()] = PALETA["destaque"]
    barras = ax.bar(
        dias_label,
        fat_diasem["VALOR_VENDA"],
        color=cores,
        edgecolor="white",
        width=0.6,
    )
    rotular_barras_v(ax, barras, offset=300)
    ax.set_title("Faturamento por Dia da Semana")
    ax.set_ylabel("Faturamento (R$)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_reais))

    ax = axes[0, 1]
    horas = [str(hora) for hora in fat_horario["FAIXA_HORARIO"]]
    barras = ax.bar(
        horas,
        fat_horario["VALOR_VENDA"],
        color=PALETA["roxo"],
        edgecolor="white",
        width=0.6,
    )
    rotular_barras_v(ax, barras, offset=300)
    ax.set_title("Faturamento por Faixa de Horario")
    ax.set_xlabel("Horario")
    ax.set_ylabel("Faturamento (R$)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_reais))

    ax = axes[1, 0]
    ticket_s = ticket.sort_values("TICKET_MEDIO", ascending=True)
    ax.barh(
        range(len(ticket_s)),
        ticket_s["TICKET_MEDIO"],
        color=PALETA["secundaria"],
        edgecolor="white",
        height=0.6,
    )
    ax.set_yticks(range(len(ticket_s)))
    ax.set_yticklabels(ticket_s["NOME_PRODUTO"])
    for i, (_, row) in enumerate(ticket_s.iterrows()):
        ax.text(
            row["TICKET_MEDIO"] + 0.2,
            i,
            f"R$ {row['TICKET_MEDIO']:.2f}",
            va="center",
            fontsize=10,
            fontweight="bold",
        )
    ax.set_title("Ticket Medio por Produto")
    ax.set_xlabel("Ticket Medio (R$)")

    ax = axes[1, 1]
    sns.heatmap(
        pivot,
        annot=True,
        fmt=",.0f",
        cmap="YlOrRd",
        ax=ax,
        linewidths=0.5,
        cbar_kws={"label": "Faturamento (R$)"},
    )
    ax.set_title("Heatmap: Horario x Dia da Semana")
    ax.set_ylabel("Faixa de Horario")
    ax.set_xlabel("Dia da Semana")

    plt.tight_layout()

    dia_fraco = fat_diasem.loc[fat_diasem["VALOR_VENDA"].idxmin()]
    dia_forte = fat_diasem.loc[fat_diasem["VALOR_VENDA"].idxmax()]
    hora_fraca = fat_horario.loc[fat_horario["VALOR_VENDA"].idxmin()]
    hora_forte = fat_horario.loc[fat_horario["VALOR_VENDA"].idxmax()]

    print("\n[DESAFIO 5] Indicadores para Estrategias")
    print(
        f"  Dia mais forte...: {DIAS_PT[dia_forte['DIA_SEMANA']]} "
        f"({fmt_reais_dec(dia_forte['VALOR_VENDA'])})"
    )
    print(
        f"  Dia mais fraco...: {DIAS_PT[dia_fraco['DIA_SEMANA']]} "
        f"({fmt_reais_dec(dia_fraco['VALOR_VENDA'])})"
    )
    print(
        f"  Horario mais forte: {hora_forte['FAIXA_HORARIO']} "
        f"({fmt_reais_dec(hora_forte['VALOR_VENDA'])})"
    )
    print(
        f"  Horario mais fraco: {hora_fraca['FAIXA_HORARIO']} "
        f"({fmt_reais_dec(hora_fraca['VALOR_VENDA'])})"
    )

    print("\n  Estrategias sugeridas:")
    sugestoes = [
        f"Promocoes as {DIAS_PT[dia_fraco['DIA_SEMANA']]}s com combos ou descontos progressivos.",
        f"Acoes no horario das {hora_fraca['FAIXA_HORARIO']}: degustacoes ou descontos-relampago.",
        "Cross-selling com frutas premium e populares em kits.",
        "Programa de fidelidade simples para incentivar recorrencia.",
        f"Reforcar estoque nos horarios de pico ({hora_forte['FAIXA_HORARIO']}).",
        "Monitorar tendencias mensais para ajustar compras e campanhas.",
    ]
    for i, estrategia in enumerate(sugestoes, 1):
        print(f"    {i}. {estrategia}")

    return fig
