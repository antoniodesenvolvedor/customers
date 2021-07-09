import os

from dotenv import load_dotenv

load_dotenv()

PRODUCTION = os.getenv('PRODUCTION') == '1'

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_HOST = 'postgres' if PRODUCTION else 'localhost'

ENCRYPT_KEY = os.getenv('ENCRYPT_KEY')

TOKEN_KEY = os.getenv('TOKEN_KEY')
TOKEN_ALGORITHM = os.getenv('TOKEN_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
