import os

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
PG_DB = os.getenv('PG_DB')
PG_USER = os.getenv('PG_USER')
PG_PASS = os.getenv('PG_PASS')
PG_HOST = os.getenv('PG_HOST')
ADMIN = os.getenv('ADMIN_ID')