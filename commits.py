import os
from dotenv import load_dotenv

load_dotenv()

commitListPath = os.getenv("COMMIT_LIST")
def getCommits():
    commitListFile = open(commitListPath, 'r')
    commits = []
    for c in commitListFile:
        commits.append(c.strip())
    return commits
