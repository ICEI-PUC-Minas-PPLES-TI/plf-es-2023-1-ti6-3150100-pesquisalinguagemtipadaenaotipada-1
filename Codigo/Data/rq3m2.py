# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.stats import kruskal

# # Lista dos nomes dos arquivos CSV
# arquivos_csv = ['Codigo/Output/JavascriptRepos/JS_repositories.csv', 'Codigo/Output/PythonRepos/py_repositories.csv',
#                 'Codigo/Output/TypescriptRepos/ts_repositories.csv', 'Codigo/Output/JavaRepos/java_repositories.csv']

# # Lista para armazenar os dados de CommitsPerPullrequests para cada arquivo
# dados_commits = []

# # Lista para armazenar os dados de language para cada arquivo
# dados_language = []

# # Função para remover outliers usando a regra do IQR
# def remover_outliers(dados):
#     q1 = np.percentile(dados, 25)
#     q3 = np.percentile(dados, 75)
#     iqr = q3 - q1
#     lim_inf = q1 - 1.5 * iqr
#     lim_sup = q3 + 1.5 * iqr
#     return [dado for dado in dados if lim_inf <= dado <= lim_sup]

# # Leitura dos arquivos CSV e extração dos dados
# for arquivo in arquivos_csv:
#     df = pd.read_csv(arquivo)
#     commits = df['medianBugFixTime']
#     # commits_sem_outliers = remover_outliers(commits)
#     # commits_log = np.log10(commits)  # Aplica escala logarítmica
#     language = df['language'].iloc[0]
#     dados_commits.append(commits)
#     dados_language.append(language)

# # Realizar o teste de Kruskal-Wallis
# statistic, p_value = kruskal(*dados_commits)

# # Mapeamento de cores para cada linguagem
# cores = {
#     'Java': '#b954a0',
#     'Python': '#8265ce',
#     'Typescript': '#1a73e8',
#     'Javascript': '#13b29a'
# }

# # Plotagem do ECDF
# plt.figure(figsize=(10, 6))

# # Dados a serem plotados
# for i, dados in enumerate(dados_commits):
#     language = dados_language[i]
#     sorted_data = np.sort(dados)
#     y_values = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
#     plt.scatter(sorted_data, y_values, label=language, color=cores[language], s=10)

# # Configurações do gráfico
# plt.xlabel('Mediana do total de issues de tipo Bug (Log Scale)')
# plt.ylabel('ECDF')
# plt.title(f'ECDF de Mediana do tempo de correção de issues de Bug por Linguagem\nKruskal-Wallis p-value = {p_value:.4f}')
# plt.grid(True)
# plt.legend()

# # Configuração da escala logarítmica de base 10
# plt.xscale('log')

# # Salvar o gráfico em uma imagem
# plt.savefig('ecdf_rq32.png')

# # Exibir o gráfico
# plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

# Lista dos nomes dos arquivos CSV
arquivos_csv = ['Codigo/Output/TypeRepos/typerepos.csv', 'Codigo/Output/NoTypeRepos/notyperepos.csv']

# Lista para armazenar os dados de total_issues para cada arquivo
dados_total_issues = []

# Lista para armazenar os dados de TipadaOuNaoTipada para cada arquivo
dados_group = []

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
    total_issues = df['medianBugFixTime']
    # total_issues_sem_outliers = remover_outliers(total_issues)
    # total_issues_log = np.log10(total_issues)  # Aplica escala logarítmica
    tipadaounao = df['TipadaOuNaoTipada'].iloc[0]
    dados_total_issues.append(total_issues)
    dados_group.append(tipadaounao)

# Realizar o teste de Mann-Whitney U
statistic, p_value = mannwhitneyu(dados_total_issues[0], dados_total_issues[1])

# Mapeamento de cores para cada grupo
cores = {
    'Tipada': '#703DCA',
    'NaoTipada': '#DF2A11',
}

# Plotagem do ECDF
plt.figure(figsize=(10, 6))

# Dados a serem plotados
for i, dados in enumerate(dados_total_issues):
    group = dados_group[i]
    sorted_data = np.sort(dados)
    y_values = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    plt.scatter(sorted_data, y_values, label=group, color=cores[group], s=10)

# Configurações do gráfico
plt.xlabel('Mediana do tempo de correção de issues de tipo Bug (Log Scale)')
plt.ylabel('ECDF')
plt.title(f'ECDF de Mediana do tempo de correção de issues de Bug por grupo \nMann-Whitney U p-value = {p_value:.4f}')
plt.grid(True)
plt.legend()

# Configuração da escala logarítmica de base 10
plt.xscale('log')

# Salvar o gráfico em uma imagem
plt.savefig('ecdf_rq32.png')

# Exibir o gráfico
plt.show()
