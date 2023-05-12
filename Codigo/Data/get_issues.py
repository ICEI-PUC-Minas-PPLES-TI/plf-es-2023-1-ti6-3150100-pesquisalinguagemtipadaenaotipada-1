import pandas as pd
import Data.repoQuery as repoQuery
from Data.mineRunner import mine_runner


def generate_issues_csv(num_repos: int, language: str, owner: str, name: str):
    repos = []
    after = 'null'
    temp_repos = []
    mediana = 0 
    clossedIssuesTotalcount = 0
    query = repoQuery.query_pr
    while len(temp_repos) < num_repos:
        data = mine_runner(query.replace("""{owner}""", f"""{owner}""").replace(
            """{name}""", f"""{name}"""))['data']['repository']['issues']
        totalCount = data['pullRequests']['totalCount']
        after = f'"{data["pageInfo"]["endCursor"]}"'
        has_next_page = data['pageInfo']['hasNextPage']
        if not has_next_page:
            break

    repos.extend(temp_repos)

    # atualizar o arquivo csv do repositório principal
    main_repo_file = f'Codigo/Output/{language.capitalize()}Repos/repositories.csv'
    main_repo_df = pd.read_csv(main_repo_file)
    main_repo_df.loc[main_repo_df['nameWithOwner'] ==
                     f"{owner}/{name}", 'medianBugFixTime'] = mediana   
    main_repo_df.loc[main_repo_df['nameWithOwner'] ==
                     f"{owner}/{name}", 'clossedIssues'] = clossedIssuesTotalcount
    main_repo_df.to_csv(main_repo_file, index=False)

    return [f'Codigo/Output/{language.capitalize()}Repos/issues_{owner}-{name}.csv']
