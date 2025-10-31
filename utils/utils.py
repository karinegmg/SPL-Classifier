import os
from dotenv import load_dotenv

COMMIT_LIST = "COMMIT_LIST"
REPOSITORY_PATH = "REPOSITORY_PATH"
OUTPUT_FILE = "OUTPUT_FILE"
SINGLE_COMMIT = "SINGLE_COMMIT"

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = f'{CURRENT_PATH}/env/.envExample'

load_dotenv(ENV_FILE)

def getVarFromEnv(var):
    return str(os.getenv(var))