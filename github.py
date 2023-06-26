import requests
from setup import load_credentials, load_target

def fetchComments():
    credentials = load_credentials()
    target = load_target()
    REPO_OWNER = target['github_repo']
    REPO_NAME = target['github_repo_owner']
    USER = target['github_user']
    OUTPUT_FILE = 'text/pull_comments.txt'
    TOKEN=credentials['github_oauth_token']


    pulls_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls?state=closed&per_page=100"
    headers = {'Authorization': f'token {TOKEN}'}

    try:
        with open('text/pull_comments.txt', 'w') as file:
            file.write('')
    except Exception as e:
        print(f"Error cleaning cleanup document: {e}")
        exit(1)

    page = 0
    print("fetching comments")
    # How many pages of pr's we look at.
    while(page<10):
        try:
            pulls_response = requests.get(pulls_url + f'&page={page}', headers=headers)
        except Exception as e:
            print("Error with getting comments: {e}")
        page+=1
        if pulls_response.status_code == 200:
            pull_requests = pulls_response.json()
            if not pull_requests:
                break

            with open(OUTPUT_FILE, 'a') as f:
                
                for pr in pull_requests:
                    
                    if pr['user']['login'] != USER:
                        continue
                    comments_url = pr['comments_url']
                    comments_response = requests.get(comments_url, headers=headers)

                    if comments_response.status_code == 200:
                        comments = comments_response.json()

                        for comment in comments:
                            if comment['user']['login'] == pr['user']['login']:
                                continue

                            # f.write(f"Pull Request: {pr['html_url']}\n")
                            # f.write(f"Comment by {comment['user']['login']} at {comment['created_at']}:\n")
                            f.write(f"comment: {comment['body']}\n")
                    else:
                        print(f"Failed to fetch comments for pull request {pr['number']}: {comments_response.status_code}")
                    
        else:
            print(f"Failed to fetch pull requests: {pulls_response.status_code}")
            print(pulls_response.content)