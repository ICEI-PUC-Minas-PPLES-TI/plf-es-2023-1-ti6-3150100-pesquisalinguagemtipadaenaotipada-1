import os
import shutil
import subprocess
from datetime import datetime as dt
import multiprocessing as mul
import os
import stat
from subprocess import call
import time

import pandas as pd
from git import Repo
import Data.repositories as repos
from Data.createSonarProject import runSonar
from Data.uploadSonar import uploadSonar

from git import Repo

NUM_REPO = 1
REPOS_FOLDER = 'Codigo/Data/repos/'
OUTPUT_FOLDER = 'Codigo/Output/'

JS_INPUT_FILE = 'Codigo/Output/JavascriptRepos/repositories.csv'
TS_INPUT_FILE = 'Codigo/Output/TypescriptRepos/repositories.csv'
PY_INPUT_FILE = 'Codigo/Output/PythonRepos/repositories.csv'
JAVA_INPUT_FILE = 'Codigo/Output/JavaRepos/repositories.csv'
OUTPUT = 'Codigo/Output/analysis.csv'

COLUMNS = ['nameWithOwner', 'url', 'stargazers',
           'mentionableUsers', 'CommitsCount', 'openIssues', 'closedIssues', 'commitsCount', 'codeSmell', 'Complexity']

startDockerCommand = ['docker', 'run', '-d', '--name', 'sonarqube', '-e',
                      'SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true', '-p', '9000:9000', 'sonarqube:latest']


# Função para mudar as permissões de escrita do arquivo ou diretório especificado pelo caminho path e, em seguida, tenta remove-lo.
def on_rm_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)


def cloneRepositories(nameWithOwner: str, url: str, stargazers: int, mentionableUsers: int, openIssues: int,  closedIssues: int, commitsCount: int) -> None:
    try:
        repo_name = nameWithOwner.replace('/', '-')
        # delete_cached_repo_data(repo_name)

        repo_path = REPOS_FOLDER + repo_name

        # Clonagem reporitorios
        print('Cloning {}'.format(nameWithOwner))
        Repo.clone_from(url, repo_path, depth=1, filter='blob:none')

        # Exclusão da pasta .git ou .github para não interferir na análise do sonar
        if os.path.exists(repo_path):
            for subpasta in [".git", ".github"]:
                subpasta_path = os.path.join(repo_path, subpasta)
                if os.path.exists(subpasta_path):
                    shutil.rmtree(subpasta_path, onerror=on_rm_error)

        # Função de calculo de qualidade do sonar api
        runSonar(REPOS_FOLDER, repo_name)

        # Exclusão de todos os arquivos na subpasta_path
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path, onerror=on_rm_error)

    except Exception as e:
        print('Error on {}: {}'.format(nameWithOwner, e))
        # delete_cached_repo_data(repo_name)


def main(num_repos: int, languages: list[str]):
    # Executa o comando de inicialização do docker
    subprocess.run(startDockerCommand)
    uploadSonar()

    # Mineração repositorios
    for language in languages:
        print(f'Generating {language.capitalize()} Repositories CSV...')
        repos.generate_csv(num_repos, language)

    # Obtenha o arquivo de entrada e filtre os repositórios já lidos
    rp_list = pd.read_csv(JS_INPUT_FILE)

    # Leitura do CSV
    repos_csv = pd.read_csv(JS_INPUT_FILE, sep=',')

    # Mineração issues dos repositórios
    for index, row in repos_csv.iterrows():
        # Obtém o owner e o name a partir da coluna nameWithOwner
        owner, name = row['nameWithOwner'].split('/')
        print(
            f'Generating {"Javascript"} Issues Repositories CSV for {owner}/{name}...')
        # Gera o CSV das issues do repositório atual
        repos.generate_issues_csv(
            num_repos, "Javascript", owner, name)

    # # Execute as métricas Sonar para cada repositório
    results = []
    for row in rp_list.itertuples():
        result = cloneRepositories(
            row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        if result is not None:
            results.append(result)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Generate CSV files with the most popular repositories on GitHub.')
    parser.add_argument('-n', '--num_repos', type=int,
                        default=300, help='Number of repositories to generate.')
    parser.add_argument('-l', '--languages', type=str, nargs='+', default=[
                        'java', 'python', 'typescript', 'javascript'], help='List of languages to generate repositories for.')

    args = parser.parse_args()
    main(args.num_repos, args.languages)
