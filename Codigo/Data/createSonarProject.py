import time
import os
from sonarqube import SonarQubeClient
import subprocess
import csv

GLOBAL_TOKEN = ''
filename = 'Codigo/Metrics/JavascriptRepos/qualityMetrics.csv'
Metrics_FOLDER = 'Codigo/Metrics/JavacriptRepos'
Cols = ['RepoName', 'CycleComplexity', 'CodeSmell']

def runScannerApi(directory, repo_name):
    global GLOBAL_TOKEN
    url = 'http://localhost:9000'
    projectName = f"{repo_name}"
    projectKey = f"{repo_name}"
    # projectKey = "photonstorm-phaser"
    username = "admin"
    password = "ADMIN"
    sonar = SonarQubeClient(
        sonarqube_url=url, username=username, password=password)
    sonar.projects.create_project(
        project=projectKey, name=projectName, visibility="public")
    user_token = sonar.user_tokens.generate_user_token(
        name=projectName, projectKey=projectKey, type="PROJECT_ANALYSIS_TOKEN")
    GLOBAL_TOKEN = user_token['token']
    print('TOKEN--------------', GLOBAL_TOKEN)

    time.sleep(5)

    # # Comando que será executado no PowerShell
    # ## - Projetos outras linguagens
    comando = f'sonar-scanner.bat -D sonar.projectKey={projectKey} -D sonar.sources={directory}{repo_name} -D sonar.host.url=http://localhost:9000 -D sonar.token={GLOBAL_TOKEN}'
    # # # # ## - Projetos Java
    # # # # # comando= f'sonar-scanner.bat -D sonar.projectKey={projectKey} -D sonar.sources={directory}{repo_name}/Java -D sonar.java.binaries={directory}{repo_name} -D sonar.host.url=http://localhost:9000 -D sonar.token={GLOBAL_TOKEN} -D sonar.java.source=11'
    
    # # # # Abre a interface gráfica do PowerShell e executa o comando
    os.system("powershell.exe " + comando)

    time.sleep(15)

    measures_history = sonar.measures.search_measures_history(component={projectKey}, metrics='code_smells , complexity', branch="main")['measures']

    # Ordena o histórico de medidas por data e seleciona o valor mais recente
    latest_value_codeSmell = sorted(measures_history[0]['history'], key=lambda k: k['date'], reverse=True)[0]['value']
    latest_value_complexity = sorted(measures_history[1]['history'], key=lambda k: k['date'], reverse=True)[0]['value']

    # Abre o arquivo em modo de escrita e cria o objeto para escrever no arquivo
    with open(filename, mode='a', newline='') as csv_file:
        fieldnames = ['RepoName', 'CycleComplexity', 'CodeSmell']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Escreve os valores das medidas no arquivo CSV
        writer.writerow({'RepoName': projectKey, 'CycleComplexity': latest_value_complexity, 'CodeSmell': latest_value_codeSmell})

    print('Results saved to', filename)

    


def runSonar(directory, repo_name):
    directoryRoot = directory
    directories = os.listdir(directory)
    # for directory in directories:
    #     print(f"Analyzing {repo_name}")
    #     runScannerApi(directoryRoot, repo_name)
    runScannerApi(directoryRoot, repo_name)

    # runScannerApi(directoryRoot, repo_name) 

