import pandas as pd
import matplotlib.pyplot as plt

JS_INPUT_FILE = 'Codigo/Output/JavascriptRepos/repositories.csv'

# Ler o arquivo CSV
df = pd.read_csv(JS_INPUT_FILE, sep=',')

# Selecionar apenas a coluna medianBugFixTime
data = df['medianBugFixTime']

# Fazer o plot do boxplot com whiskers
fig, ax = plt.subplots()
ax.boxplot(data, whis=1.5, showfliers=False)

# Definir o título e os rótulos dos eixos
ax.set_title('Boxplot da coluna medianBugFixTime')
ax.set_ylabel('Tempo (horas)')

# Adicionar mediana no gráfico
ax.axhline(data.median(), color='red', label='Mediana')

# Adicionar mediana na legenda
mediana_str = '{:.2f}'.format(data.median())
ax.legend([f'Mediana = {mediana_str} horas'])

# Salvar o gráfico em um arquivo
plt.savefig("boxplot.png")

# Mostrar o gráfico
plt.show()
