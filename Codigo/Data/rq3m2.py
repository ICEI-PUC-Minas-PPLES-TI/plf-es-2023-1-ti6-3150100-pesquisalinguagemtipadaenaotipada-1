import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kruskal
from statsmodels.distributions.empirical_distribution import ECDF

# Lista dos nomes dos arquivos CSV
arquivos_csv = ['Codigo/Output/JavascriptRepos/repositories.csv', 'Codigo/Output/PythonRepos/repositories.csv',
                'Codigo/Output/TypescriptRepos/repositories.csv', 'Codigo/Output/JavaRepos/repositories.csv']

# Lista para armazenar os dados de openIssues + closedIssues para cada arquivo
dados_issues = []

# Lista para armazenar os dados de language para cada arquivo
dados_language = []

# Função para remover outliers usando a regra do IQR
def remover_outliers(dados):
    q1 = np.percentile(dados, 25)
    q3 = np.percentile(dados, 75)
    iqr = q3 - q1
    lim_inf = q1 - 1.5 * iqr
    lim_sup = q3 + 1.5 * iqr
    return [dado for dado in dados if lim_inf <= dado <= lim_sup]

# Leitura dos arquivos CSV e extração dos dados
for arquivo in arquivos_csv:
    df = pd.read_csv(arquivo)
    open_issues = df['openIssues']
    closed_issues = df['clossedIssues']
    issues = open_issues + closed_issues
    # issues_sem_outliers = remover_outliers(issues)
    language = df['language']
    dados_issues.append(issues)
    dados_language.append(language)

# Realizar o teste de Kruskal-Wallis
statistic, p_value = kruskal(*dados_issues)

# Mapeamento de cores para cada linguagem
cores = {
    'Java': '#b954a0',
    'Python': '#8265ce',
    'Typescript': '#1a73e8',
    'Javascript': '#13b29a'
}

# Plotagem do ECDF
plt.figure(figsize=(10, 6))

# Dados a serem plotados
for i, dados in enumerate(dados_issues):
    language = dados_language[i].iloc[0]
    ecdf = ECDF(dados)
    plt.plot(ecdf.x, ecdf.y, label=language, color=cores[language])

# Configurações do gráfico
plt.xlabel('Open Issues + Clossed Issues')
plt.ylabel('ECDF')
plt.title(f'ECDF de Soma de Issues Abertas e Fechadas por Linguagem\nKruskal-Wallis p-value = {p_value:.4f}')
plt.grid(True)
plt.legend()

# Configuração da escala logarítmica de base 10
plt.xscale('log')

# Salvar o gráfico em uma imagem
plt.savefig('ecdf_rq32.png')

# Exibir o gráfico
plt.show()
