import pandas as pd
from scipy import stats

# Carregar os dados dos CSVs em dataframes do pandas
df1 = pd.read_csv('Codigo/Output/TypeRepos/typerepos.csv')
df2 = pd.read_csv('Codigo/Output/NoTypeRepos/notyperepos.csv')



# Extrair as colunas "CodeSmell" dos dataframes
coluna1 = df1['medianBugFixTime']
coluna2 = df2['medianBugFixTime']

# Executar o teste de Shapiro-Wilk
_, p_value1 = stats.shapiro(coluna1)
_, p_value2 = stats.shapiro(coluna2)

# Imprimir os resultados
print("Resultados do Teste de Shapiro-Wilk:")
print("CSV 1 - p-value:", p_value1)
print("CSV 2 - p-value:", p_value2)

# # Executar o teste de Mann-Whitney U
# _, p_value = stats.mannwhitneyu(coluna1, coluna2)

# # Imprimir o resultado
# print("Resultado do Teste de Mann-Whitney U:")
# print("p-value:", p_value)