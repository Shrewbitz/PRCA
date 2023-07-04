
from urllib.parse import urlparse


def target_setup(github_user, github_repo_site): 
    parsed_url = urlparse(github_repo_site)
    if parsed_url[1] != "github.com":
        print("incorrect URL")
        return
    path_parts = parsed_url.path.lstrip('/').split('/')
    github_repo = path_parts[0]
    github_repo_owner = path_parts[1]

    return {
        "github_repo": github_repo,
        "github_repo_owner": github_repo_owner,
        "github_user": github_user,
    }


