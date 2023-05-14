from os import getenv
from dotenv import load_dotenv

load_dotenv(dotenv_path="env\\venv.env")
def get_token():
    token = getenv('TOKEN_API')
    return token

def get_path():
    path = getenv('PATH')
    return path
