import sys
import time
from setup import setup, target_setup
from github import fetchComments
from gpt_analysis import analyze_github_comments, summarize_feedback

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py [setup|analyze]")
        sys.exit(1)

    if sys.argv[1] == "setup":
        setup()
    elif sys.argv[1] == "analyze":
        target_setup()
        fetchComments()
        time.sleep(1)
        analyze_github_comments()
        time.sleep(1)
        summarize_feedback()
    else:
        print("Invalid argument. Usage: python3 main.py [setup|analyze]")
        sys.exit(1)

if __name__ == "__main__":
    main()