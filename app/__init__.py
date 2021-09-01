from random import randint
from flask import Flask
from flask_login import LoginManager


class Settings:
    APP_ID = ''.join(["{}".format(randint(0, 9)) for num in range(0, 6)])
    AD_IP_ADDR = ''
    EXTERNAL_LINK = ''
    DB_CONN_STRING = ''
    STORAGE_PATH = ''


app = Flask(__name__)

app.config['SECRET_KEY'] = "secret_key"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False

login_manager = LoginManager()
login_manager.login_view = 'login_post'
login_manager.init_app(app)

