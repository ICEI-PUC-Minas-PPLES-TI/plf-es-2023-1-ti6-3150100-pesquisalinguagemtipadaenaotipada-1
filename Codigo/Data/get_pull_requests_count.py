import pandas as pd
import os
import requests


from dotenv import load_dotenv
import os
from random import randint
import requests
from time import sleep
load_dotenv()  # load secrets from .env

MAX_QUERY_ATTEMPTS = 10
GITHUB_INDEX = 0
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN_1')
filename = 'Codigo/Output/JSthonRepos/JSthonRepositories.csv'

# Função para fazer a chamada à API do GitHub e retornar o total de pull requests

query_pr = """
  {
    repository(owner: "{owner}", name: "{name}") {
    pullRequests {
            totalCount
            }
  }
  }
"""
def mine_runner(query: str, attemp=1) -> dict:
    """
    This function runs a query against the GitHub GraphQL API and returns the result.
    """
    url = 'https://api.github.com/graphql'
    global GITHUB_INDEX
    token = GITHUB_TOKEN
    headers = {'Authorization': 'Bearer {}'.format(token)}
    try:
        response = requests.post(url, json={'query': query}, headers=headers)
        print(response)
        remaining_requests = response.headers.get('x-ratelimit-remaining')
        message = ("Response: ", response.status_code, " -> ",
                   response.json(), "\n") if not remaining_requests else None
        print(
            f'{message}',
        )
        if not remaining_requests and response.status_code in (403, 502):
            sleep(60)
            return mine_runner(query, attemp)
        if remaining_requests <= '1':
            print('Renewing token...')
            GITHUB_INDEX = (GITHUB_INDEX + 1) % len(GITHUB_TOKEN)
            return mine_runner(query, attemp)

        elif response.status_code == 200:
            return response.json()

        elif response.status_code == 502 and attemp <= MAX_QUERY_ATTEMPTS:
            print(
                'Attemp {}/{} get Error 502. Retrying...'.format(attemp, MAX_QUERY_ATTEMPTS))
            return mine_runner(query, attemp + 1)

        elif response.status_code == 502 and attemp > MAX_QUERY_ATTEMPTS:
            print('Error 502. Maximum number of attempts reached. Try again later.')
            exit(1)

        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(
                response.status_code, query))

    except Exception as e:
        print(e)
        return mine_runner(query, attemp)


def get_pull_requests_count():
    
    # carrega arquivo CSV
    df = pd.read_csv('Codigo/Output/JavaRepos/Java1 - Java1.csv')

    # remover a coluna "medianBugFixTime"
    # df = df.drop('medianBugFixTime', axis=1)

    # adicionar uma nova coluna chamada "language" com valor "Javascript"
    df['TipadaOuNaoTipada'] = 'Tipada'

    # # salvar o arquivo CSV atualizado
    df.to_csv('Codigo/Output/JavaRepos/Java1 - Java1.csv', index=False)


    # # itera sobre as linhas do DataFrame
    # for index, row in df.iterrows():
    #     # separa o name e o owner do nameWithOwner
    #     owner, name = row['nameWithOwner'].split('/')
    #     # preenche a query com os valores de owner e name
    #     query = query_pr.replace("""{owner}""", f"""{owner}""").replace("""{name}""", f"""{name}""")
    #     # realiza a mineração com a função mine_runner
    #     result = mine_runner(query)
    #     # obtém o valor de totalCount de pullRequests do resultado da mineração
    #     pullrequests_count = result['data']['repository']['pullRequests']['totalCount']
    #     # atualiza a coluna pullrequestsCount da linha correspondente
    #     df.at[index, 'pullrequestsCount'] = pullrequests_count

    # # salva as alterações no arquivo CSV
    # df.to_csv('Codigo/Output/JavaRepos/repositories.csv', index=False)