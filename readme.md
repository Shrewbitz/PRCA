# PRCA - pull request comment analysis

This program will look through pull requests made by a user, it will collect comments made by other users. The comments are sent to gpt3.5 for analysis. We return all of the gpt3.5's analysis to gpt3.5 to summarize. It will then return the final feedback in 3_summary.txt


## Usage:
### Things you will need:
- open ai secret key
- github oauth token
- the url of the repo you want to get comments from
- the username of the github user you wish to analyze

### Installation:
- clone the repo
- install python 3.x
- pip install getpass
- pip install openai

### Commands:
- python3 main.py setup (will only need to run once)
- python3 main.py analyze (run everytime you wish to analyze a user)

### How to use:
- Run the setup command. It will prompt you for a secret key and an oauth token then store them in creds.json
- Next run the analyze command. 
- It will prompt you for a repo: https://github.com/facebook/react-native and a github username: coolprogrammer21.
- As it runs the text folder files will appear. it will first create the pull_comments.txt file.
- Once it has gathered the comments it will send batches of the raw comments to gpt3.5 and append the responses to feedback.txt
- Finally it will send the feedback to gpt3.5 to be summarized. 
- All of these text files are available to look at.

nextgoal1 - figure out how to analyze feedback without losing context of batching
nextgoal2 - let it prompt you for multiple repos
nextgoal3 - is to use python server / website 