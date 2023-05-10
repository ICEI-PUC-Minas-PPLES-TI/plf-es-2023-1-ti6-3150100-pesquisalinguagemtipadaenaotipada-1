import pandas as pd
import matplotlib.pyplot as plt

JS_INPUT_FILE = 'Codigo/Metrics/JavascriptRepos/qualityMetrics.csv'

# Ler o arquivo CSV
df = pd.read_csv(JS_INPUT_FILE, sep=',')

# Selecionar apenas as colunas CycleComplexity e CodeSmell
data_cycle_complexity = df['CycleComplexity']
data_code_smell = df['CodeSmell']

# Calcular a mediana de cada coluna
median_cycle_complexity = data_cycle_complexity.median()
median_code_smell = data_code_smell.median()

# Fazer o plot do boxplot com whiskers
fig, ax = plt.subplots()
ax.boxplot([data_cycle_complexity, data_code_smell], labels=['CycleComplexity', 'CodeSmell'], whis=1.5, showfliers=False)

# Definir o título e os rótulos dos eixos
ax.set_title('Boxplot das colunas CycleComplexity e CodeSmell')
ax.set_ylabel('Valores')

# Adicionar mediana no gráfico
ax.axhline(median_cycle_complexity, color='red', label='Mediana CycleComplexity: {:.2f}'.format(median_cycle_complexity))
ax.axhline(median_code_smell, color='green', label='Mediana CodeSmell: {:.2f}'.format(median_code_smell))
ax.legend()

# Salvar o gráfico em um arquivo
plt.savefig("boxplot.png")

# Mostrar o gráfico
plt.show()


