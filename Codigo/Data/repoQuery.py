repositories_query = """
  {
  search(query: "stars:>100 language:{language} sort:stars", type: REPOSITORY, first: 25, after: {after}) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      ... on Repository {
        nameWithOwner
        url
        stargazers {
          totalCount
        }
        mentionableUsers {
          totalCount
        }
        defaultBranchRef {
          target {
            ... on Commit {
              history {
                totalCount
              }
            }
          }
        }
        openIssues: issues(states: OPEN, labels: ["Type: bug", "bug", "error", "fix"]) {
          totalCount
        }
      }
    }
  }
}
    """


query_issues = """
  {
    repository(owner: "{owner}", name: "{name}") {
    issues(last: 100, states: CLOSED, labels: ["Type: bug", "bug", "error", "fix"], after: {after}) {
     pageInfo {
        hasNextPage
        endCursor
      }
      totalCount
      edges {
        node {
          createdAt
          closedAt
        }
      }
    }
  }
  }
"""
query_pr = """
  {
    repository(owner: "{owner}", name: "{name}") {
    pullRequests {
            totalCount
            }
  }
  }
"""