from random import randint
from flask import Flask


class Settings:
    APP_ID = ''.join(["{}".format(randint(0, 9)) for num in range(0, 6)])
    AD_IP_ADDR = '' # '192.168.0.7'
    DB_CONN_STRING = '' # 'postgresql://postgres:1234@localhost/postgres'
    STORAGE_PATH = '' # '/'


app = Flask(__name__)
