import sqlite3
import pandas as pd
import matplotlib.pyplot as mplt
from matplotlib.ticker import FuncFormatter
from flet.matplotlib_chart import MatplotlibChart


# ============================================================================================================================================

""" FUNÇÃO QUE CRIA O GRÁFICO DE LINHAS DO FINANCEIRO """

# ============================================================================================================================================


def grafico_linhas(dark):
    # Define o estilo do gráfico com base no modo (dark ou light)
    estilo_dark = {
        'axes.facecolor': '#1a1c1e',
        'axes.edgecolor': '#CCCCCC',
        'axes.labelcolor': '#CCCCCC',
        'xtick.color': '#CCCCCC',
        'ytick.color': '#CCCCCC',
        'grid.color': '#333333',
        'figure.facecolor': '#1a1c1e',
        'text.color': '#CCCCCC'
    }
    estilo_light = {
        'axes.facecolor': '#fdfcff',
        'axes.edgecolor': '#CCCCCC',
        'axes.labelcolor': '#CCCCCC',
        'xtick.color': '#333333',
        'ytick.color': '#333333',
        'grid.color': '#333333',
        'figure.facecolor': '#fdfcff',
        'text.color': '#333333'
    }

    mplt.style.use(estilo_dark if dark == "dark" else estilo_light)

    # Conecta ao banco de dados SQLite
    conn = sqlite3.connect("BD.sqlite3")

    # Query dos dados da tabela FinanceiroAlugueis / utilizando pandas para melhor leitura de dados 
    df = pd.read_sql_query("SELECT lucro_admin, liquido_empresa FROM FinanceiroAlugueis", conn)

    # Query dos dados da tabela FinanceiroDividas / utilizando pandas para melhor leitura de dados 
    df2 = pd.read_sql_query("SELECT saida FROM FinanceiroDividas", conn)

    # Cria a figura e os eixos, ajustes de tamanho e layouts
    fig, ax = mplt.subplots(figsize=(12, 4), constrained_layout=True)

    # Plota as linhas no gráfico, com base nos dados da query tratada pelo Pandas
    linhas = [
        ax.plot(df["liquido_empresa"], label="Lucros Empresa", marker='o', linestyle='-', linewidth=2, color='green')[0],
        ax.plot(df2["saida"], label="Dívidas e Gastos", marker='o', linestyle='-', linewidth=2, color='red')[0],
        ax.plot(df["lucro_admin"], label="Lucros Administração", marker='o', linestyle=':', linewidth=2, color='orange')[0]
    ]

    # Formatação do eixo Y
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"${value:.2f}"))
    ax.yaxis.set_tick_params(labelsize=5)

    # Formatação do eixo X
    ax.xaxis.set_tick_params(labelsize=5)

    # Adiciona o título à esquerda e formata fonte, espessura, nome
    ax.set_title("\nGráficos Financeiros (US$)", fontsize=9, fontweight='bold', loc='left')

    # Adiciona a legenda dentro do gráfico, formata fonte e nomes
    ax.legend(linhas, ["Lucros Empresa", "Dívidas e Gastos", "Lucros Administração"], loc='upper right', fontsize=5, bbox_to_anchor=(1, 1))

    # Adiciona a grade no eixo Y com formatações especificas, como estilo da linha e espessura
    mplt.grid(axis='y', linestyle='--', linewidth=0.5)

    # Retorna o gráfico como objeto MatplotlibChart para a renderização do flet na chamada da função
    return MatplotlibChart(fig, expand=True)


# ============================================================================================================================================

""" FUNÇÃO QUE CRIA O GRÁFICO DE LINHAS DOS ALUGUÉIS"""

# ============================================================================================================================================


def grafico_linhas2():
    conexao = sqlite3.connect('BD.sqlite3')

    # Consulta SQL para obter os dados da tabela "historico"
    consulta_sql = "SELECT data_retirada FROM historico"

    # Executa a consulta e cria um DataFrame / com utilização do pandas
    df_historico = pd.read_sql_query(consulta_sql, conexao)

    # Criando um DataFrame a partir dos dados / com utilização do pandas
    df_historico = pd.DataFrame(df_historico)

    # Convertendo a string de data para o formato de datetime (formato brasileiro)
    df_historico['data_retirada'] = pd.to_datetime(df_historico['data_retirada'], format='%d/%m/%Y')

    # Contagem dos aluguéis por dia
    contagem_alugueis = df_historico['data_retirada'].value_counts().sort_index()

    # Criando o gráfico de linha
    fig, ax = mplt.subplots(figsize=(12, 2), constrained_layout=True)

    dias = contagem_alugueis.index
    quantidade_alugueis = contagem_alugueis.values

    # Plota as linhas no gráfico
    linhas = [ax.plot(dias, quantidade_alugueis, label="Quantidade de Aluguéis", marker='o', linestyle='-', linewidth=2, color='#003377')[0]]
    
    # Formatação do eixo Y
    ax.yaxis.set_tick_params(labelsize=5)
    ax.yaxis.set_major_locator(mplt.MaxNLocator(integer=True))

    # Formatação do eixo X
    ax.xaxis.set_major_formatter(mplt.matplotlib.dates.DateFormatter('%d/%m/%Y'))
    ax.xaxis.set_tick_params(labelsize=5)

    # Adiciona o título à esquerda
    ax.set_title("\nQuantidade de Aluguéis por Dia", fontsize=9, fontweight='bold', loc='left')

    # Adiciona a legenda dentro do gráfico
    ax.legend(linhas, ["Quantidade de Aluguéis"], loc='upper right', bbox_to_anchor=(1, 1), fontsize=5)

    # Adiciona a grade no eixo Y
    mplt.grid(axis='y', linestyle='--', linewidth=0.5)

    return MatplotlibChart(fig, expand=True)

# ============================================================================================================================================
