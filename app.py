import os
from setup import target_setup
from github import fetchComments
from gpt_analysis import analyze_github_comments, summarize_feedback
from flask import Flask, request, jsonify
from flask_cors import CORS
from redis import Redis
from rq import Queue
import logging

logging.basicConfig(level=logging.DEBUG)

# redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

redis_url = os.getenv('REDIS_URL', 'redis://')
redis_conn = Redis.from_url(redis_url)
q = Queue(connection=redis_conn)


app = Flask(__name__)
CORS(app)
@app.route('/')
def home():
    return 'Welcome to PRCA!'

def analyze(credentials, target):
    logging.debug("fetching comments")
    comments = fetchComments(credentials, target)
    logging.debug("analyzing github comments")
    feedback = analyze_github_comments(credentials, comments)
    logging.debug("summarizing feedback")
    summary = summarize_feedback(credentials, feedback)
    return summary

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
    logging.debug("made it to enqueue")
    print("print enqueue")
    job = q.enqueue(analyze, credentials, target)
    
    return jsonify({"job_id": job.get_id()}), 202

# use single quotes
@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    try:
        job = q.fetch_job(job_key)
        if job.is_finished:
            return jsonify(job.result), 200
        else: 
            return "Job in progress", 202
    except:
        return "No such job", 404

if __name__ == "__main__":
    app.run(debug=True)