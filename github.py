import requests

def fetchComments(credentials, target):
    REPO_OWNER = target['github_repo']
    REPO_NAME = target['github_repo_owner']
    USER = target['github_user']
    TOKEN=credentials['github_oauth_token']

    pulls_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls?state=closed&per_page=100"
    headers = {'Authorization': f'token {TOKEN}'}

    page = 0
    print("fetching comments")
    # How many pages of pr's we look at.
    while(page<5):
        try:
            pulls_response = requests.get(pulls_url + f'&page={page}', headers=headers)
        except Exception as e:
            print("Error with getting comments: {e}")
        page+=1
        if pulls_response.status_code == 200:
            pull_requests = pulls_response.json()
            if not pull_requests:
                break       
            for pr in pull_requests:
                    
                if pr['user']['login'] != USER:
                    continue
                comments_url = pr['comments_url']
                comments_response = requests.get(comments_url, headers=headers)
                if comments_response.status_code == 200:
                    comments = comments_response.json()
                    comment_arr = []
                    for comment in comments:
                        if comment['user']['login'] == pr['user']['login']:
                            continue
                        comment_arr.append(comment['body'])
                    return "\n".join(comment_arr)
                else:
                    print(f"Failed to fetch comments for pull request {pr['number']}: {comments_response.status_code}")
                        
        else:
            print(f"Failed to fetch pull requests: {pulls_response.status_code}")
            print(pulls_response.content)