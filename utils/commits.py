from utils.utils import *

commitListFile = getVarFromEnv(COMMIT_LIST)
commitListPath = f"{CURRENT_PATH}/config_files/{commitListFile}"

def getCommits():
    commitListFile = open(commitListPath, 'r')
    commits = []
    for c in commitListFile:
        commits.append(c.strip())
    return commits
