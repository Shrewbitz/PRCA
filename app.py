import os
from setup import target_setup
from github import fetchComments
from gpt_analysis import analyze_github_comments, summarize_feedback
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/')
def home():
    return 'Welcome to PRCA!'

@app.route('/analyze', methods=['POST'])

def analyze_repo():
    data = request.get_json(force=True)

    password = os.getenv('PRCA_PASSWORD')
    github_oauth_token = os.getenv('GITHUB_OAUTH_TOKEN')
    openai_secret_key = os.getenv('OPENAI_SECRET_KEY')
    if data['password'] != password:
        return jsonify("Incorrect Credentials"), 401

    credentials = {
        "github_oauth_token": github_oauth_token,
        "openai_secret_key": openai_secret_key
    }
  
    target = target_setup(data['github_user'], data['github_repo'])

    comments = fetchComments(credentials, target)
    feedback = analyze_github_comments(credentials, comments)
    summary = summarize_feedback(credentials, feedback)
    
    return jsonify(summary), 200

if __name__ == "__main__":
    app.run(debug=True)