import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import Tk, Label, Button, filedialog

# Função para carregar dados
def carregar_dados():
    global clientes_df
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filepath:
        clientes_df = pd.read_csv(filepath, encoding='latin1')
        Label(root, text=f"Arquivo carregado: {filepath}", font=('Helvetica', 12)).pack()
        exibir_dados_resumo()

# Função para exibir resumo dos dados
def exibir_dados_resumo():
    gasto_total = clientes_df['total_gasto'].sum()
    media_gasto = clientes_df['total_gasto'].mean()
    media_compras = clientes_df['total_compras'].mean()
    produto_popular = clientes_df['produto_favorito'].value_counts().idxmax()

    Label(root, text=f"Gasto total dos clientes: R${gasto_total:.2f}", font=('Helvetica', 12)).pack()
    Label(root, text=f"Média de gasto por cliente: R${media_gasto:.2f}", font=('Helvetica', 12)).pack()
    Label(root, text=f"Média de compras por cliente: {media_compras:.2f}", font=('Helvetica', 12)).pack()
    Label(root, text=f"O produto favorito mais popular é: {produto_popular}", font=('Helvetica', 12)).pack()

# Função para salvar e exibir gráficos
def exibir_graficos():
    # Obter diretório atual
    diretório_atual = os.path.dirname(os.path.abspath(__file__))

    # Distribuição de Gênero
    plt.figure(figsize=(10, 5))
    sns.countplot(x='gênero', data=clientes_df, hue='gênero', palette='viridis', legend=False)
    plt.title('Distribuição de Gênero dos Clientes', fontsize=16)
    plt.xlabel('Gênero', fontsize=14)
    plt.ylabel('Contagem', fontsize=14)
    plt.savefig(os.path.join(diretório_atual, 'distribuicao_genero.png'))
    plt.show(block=False)

    # Distribuição de Idade
    plt.figure(figsize=(10, 5))
    sns.histplot(clientes_df['idade'], bins=15, kde=True, color='skyblue')
    plt.title('Distribuição de Idade dos Clientes', fontsize=16)
    plt.xlabel('Idade', fontsize=14)
    plt.ylabel('Contagem', fontsize=14)
    plt.savefig(os.path.join(diretório_atual, 'distribuicao_idade.png'))
    plt.show(block=False)

    # Análise de Gastos Totais e Média de Compras por Cliente
    clientes_df['total_gasto'] = clientes_df['total_gasto'].astype(float)
    clientes_df['total_compras'] = clientes_df['total_compras'].astype(int)

    # Gráfico de Linhas de Gastos Totais por Cliente
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=clientes_df, x=clientes_df.index, y='total_gasto', marker='o', color='coral')
    plt.title('Gastos Totais por Cliente', fontsize=16)
    plt.xlabel('Cliente (Index)', fontsize=14)
    plt.ylabel('Gasto Total (R$)', fontsize=14)
    plt.savefig(os.path.join(diretório_atual, 'gastos_totais_cliente.png'))
    plt.show(block=False)

    # Análise de Correlação entre Idade e Gasto Total
    plt.figure(figsize=(10, 5))
    sns.scatterplot(x='idade', y='total_gasto', data=clientes_df, color='purple')
    plt.title('Correlação entre Idade e Gasto Total', fontsize=16)
    plt.xlabel('Idade', fontsize=14)
    plt.ylabel('Gasto Total (R$)', fontsize=14)
    plt.savefig(os.path.join(diretório_atual, 'correlacao_idade_gasto.png'))
    plt.show(block=False)

    # Selecionar apenas as colunas numéricas
    numerical_cols = clientes_df.select_dtypes(include=['float64', 'int64'])

    # Correlação numérica
    correlacao = numerical_cols.corr()
    print(f"Correlação entre variáveis numéricas:\n{correlacao}")

    # Plotar matriz de correlação
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlacao, annot=True, cmap='coolwarm', vmin=-1, vmax=1, linewidths=.5)
    plt.title('Matriz de Correlação', fontsize=16)
    plt.savefig(os.path.join(diretório_atual, 'matriz_correlacao.png'))
    plt.show(block=False)

# Criar janela principal
root = Tk()
root.title("Análise de Dados BeerTruck")

# Estilizando a janela
root.geometry("600x400")
root.configure(bg='lightgrey')

# Botões para carregar dados e exibir gráficos
Button(root, text="Carregar Dados", command=carregar_dados, font=('Helvetica', 12), bg='lightblue').pack(pady=10)
Button(root, text="Exibir Gráficos", command=exibir_graficos, font=('Helvetica', 12), bg='lightgreen').pack(pady=10)

# Iniciar a aplicação
root.mainloop()
