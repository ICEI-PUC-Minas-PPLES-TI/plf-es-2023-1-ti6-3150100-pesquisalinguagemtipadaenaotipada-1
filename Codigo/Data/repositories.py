import pandas as pd
import Data.repoQuery as repoQuery
from Data.mineRunner import mine_runner


def generate_csv(num_repos: int, language: str):
    query = repoQuery.repositories_query
    repos = []
    after = 'null'
    temp_repos = []
    while len(temp_repos) < num_repos:
        data = mine_runner(query.replace('{after}', after).replace(
            '{language}', language))['data']['search']
        nodes = data['nodes']
        for repo in nodes:
            temp_repos.append({
                'nameWithOwner': repo['nameWithOwner'],
                'url': repo['url'],
                'stargazers': repo['stargazers']['totalCount'],
                'mentionableUsers': repo['mentionableUsers']['totalCount'],
                'openIssues': repo['openIssues']['totalCount'],
                'commitsCount': repo['defaultBranchRef']['target']['history']['totalCount'],
            })
        after = f'"{data["pageInfo"]["endCursor"]}"'
    repos.extend(temp_repos)

    pd.DataFrame(repos).sort_values(by='stargazers', ascending=False)[:num_repos].to_csv(
        f'Codigo/Output/{language.capitalize()}Repos/repositories.csv', index=False)

    return [f'Codigo/Output/{language.capitalize()}Repos/repositories.csv']


def generate_issues_csv(num_repos: int, language: str, owner: str, name: str):
    repos = []
    after = 'null'
    totalCount = 0
    temp_repos = []
    query = repoQuery.query_issues
    while len(temp_repos) < num_repos:
        data = mine_runner(query.replace('{after}', after).replace("""{owner}""", f"""{owner}""").replace(
            """{name}""", f"""{name}"""))['data']['repository']['issues']
        edges = data['edges']
        totalCount = data['totalCount']
        for node in edges:
            temp_repos.append({
                'createdAt': node['node']['createdAt'],
                'closedAt': node['node']['closedAt'],
            })
        after = f'"{data["pageInfo"]["endCursor"]}"'
        has_next_page = data['pageInfo']['hasNextPage']
        if not has_next_page:
            break

    repos.extend(temp_repos)

    # calcular o tempo de fechamento de cada issue em horas
    repos_df = pd.DataFrame(repos)
    repos_df["createdAt"] = pd.to_datetime(repos_df["createdAt"])
    repos_df["closedAt"] = pd.to_datetime(repos_df["closedAt"])
    repos_df["totalTime"] = repos_df.apply(lambda x: (
        x["closedAt"] - x["createdAt"]).total_seconds() / 3600, axis=1)
    repos_df.to_csv(
        f'Codigo/Output/{language.capitalize()}Repos/issues_{owner}-{name}.csv', index=False)

    # calcular a mediana
    df = pd.read_csv(
        f'Codigo/Output/{language.capitalize()}Repos/issues_{owner}-{name}.csv')
    mediana = df['totalTime'].median()

    print(f'A mediana do tempo total é de {mediana:.2f} horas.')

    # atualizar o arquivo csv do repositório principal
    main_repo_file = f'Codigo/Output/{language.capitalize()}Repos/repositories.csv'
    main_repo_df = pd.read_csv(main_repo_file)
    main_repo_df.loc[main_repo_df['nameWithOwner'] ==
                     f"{owner}/{name}", 'clossedIssues'] = totalCount
    main_repo_df.loc[main_repo_df['nameWithOwner'] ==
                     f"{owner}/{name}", 'medianBugFixTime'] = mediana
    
    main_repo_df.to_csv(main_repo_file, index=False)

    return [f'Codigo/Output/{language.capitalize()}Repos/issues_{owner}-{name}.csv']
