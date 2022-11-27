import os

from dotenv import load_dotenv
load_dotenv()

host = os.getenv('host')
user = os.getenv('user')
password = os.getenv('password')
db_name = os.getenv('db_name')
port = os.getenv('port')
