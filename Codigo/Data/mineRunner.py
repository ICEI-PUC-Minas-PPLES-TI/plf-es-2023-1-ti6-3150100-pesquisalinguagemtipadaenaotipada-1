from dotenv import load_dotenv
import os
from random import randint
import requests
from time import sleep
load_dotenv()  # load secrets from .env

MAX_QUERY_ATTEMPTS = 10
GITHUB_INDEX = 0
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN_1')


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
