import pandas as pd

# ler os dois arquivos csv
df2 = pd.read_csv('Codigo/Metrics/TypescriptRepos/qualityMetrics.csv')
df1 = pd.read_csv('Codigo/Output/TypescriptRepos/repositories.csv')

# verificar se há linhas faltando comparando "nameWithOwner" com "RepoName"
missing_rows = df1[~df1['nameWithOwner'].isin(df2['RepoName'])]

if not missing_rows.empty:
    print('As seguintes linhas estão faltando no segundo arquivo:')
    print(missing_rows)
else:
    print('Não há linhas faltando.')
