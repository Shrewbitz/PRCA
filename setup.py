import getpass
import json
import os
from urllib.parse import urlparse



def setup():
    if os.path.exists("creds.json"):
        overwrite = input("Credentials already exist. Do you want to overwrite them? (y/n): ")
        if overwrite.lower() != "y":
            print("Setup cancelled.")
            return
    github_oauth_token = getpass.getpass("Enter your GitHub Oauth token: ")
    openai_secret_key = getpass.getpass("Enter your openai_secret_key: ")

    credentials = {
        "github_oauth_token": github_oauth_token,
        "openai_secret_key": openai_secret_key,
    }

    with open("creds.json", "w") as file:
        json.dump(credentials, file)


def load_credentials():
    with open("creds.json", "r") as file:
        credentials = json.load(file)
    return credentials

def target_setup(): 
    if os.path.exists("target.json"):
        overwrite = input("Do you want to analyze a new user? (y/n): ")
        if overwrite.lower() != "y":
            return
    github_repo_site = input("Enter the URL of the repo you wish to analyze: ")
    parsed_url = urlparse(github_repo_site)
    if parsed_url[1] != "github.com":
        print("incorrect URL")
        return
    path_parts = parsed_url.path.lstrip('/').split('/')
    github_repo = path_parts[0]
    github_repo_owner = path_parts[1]
    github_user = input("Enter the username you wish to analyze: ")

    target = {
        "github_repo": github_repo,
        "github_repo_owner": github_repo_owner,
        "github_user": github_user,
    }

    with open("target.json", "w") as file:
        json.dump(target, file)

def load_target():
    with open("target.json", "r") as file:
        target = json.load(file)
    return target