import os
from dotenv import load_dotenv

load_dotenv()

FSTR_DB_LOGIN = os.getenv('FSTR_DB_LOGIN')
FSTR_DB_PASS = os.getenv('FSTR_DB_PASS')
FSTR_DB_HOST = os.getenv('FSTR_DB_HOST')
FSTR_DB_PORT = os.getenv('FSTR_DB_PORT')
FSTR_DB_NAME = os.getenv('FSTR_DB_NAME')
UVCRN_HOST = os.getenv('UVCRN_HOST')
UVCRN_PORT = os.getenv('UVCRN_PORT')
SECRET = os.getenv('SECRET')
SECRET_AUTH = os.getenv('SECRET_AUTH')
ADMIN_USER_MODEL = os.getenv('ADMIN_USER_MODEL')
ADMIN_USER_MODEL_USERNAME_FIELD = os.getenv('ADMIN_USER_MODEL_USERNAME_FIELD')
ADMIN_SECRET_KEY = os.getenv('ADMIN_SECRET_KEY')
