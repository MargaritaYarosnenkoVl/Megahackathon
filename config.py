import os
from dotenv import load_dotenv

load_dotenv()

FSTR_DB_LOGIN = os.getenv('FSTR_DB_LOGIN')
FSTR_DB_PASS = os.getenv('FSTR_DB_PASS')
FSTR_DB_HOST = os.getenv('FSTR_DB_HOST')
FSTR_DB_PORT = os.getenv('FSTR_DB_PORT')
FSTR_DB_NAME = os.getenv('FSTR_DB_NAME')
SECRET = os.getenv('SECRET')
