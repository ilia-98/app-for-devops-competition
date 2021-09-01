
from werkzeug.exceptions import abort

from app import app, Settings
from functools import wraps
from datetime import datetime
from flask import request, send_from_directory, send_file
from ldap3 import Server, Connection, ALL, NTLM
from app.database import db_session
from app.models import Messages
from time import strftime

BH_SET = False
BH_CODE = 200
LOG = ''


def manage_request(func):
    @wraps(func)
    def wrapper():
        global BH_SET
        global BH_CODE
        if BH_SET:
            abort(BH_CODE)
            # return f'Error {BH_CODE}', BH_CODE
        else:
            return func()
    return wrapper


@app.after_request
def after_request(response):
    global LOG
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    LOG += f'{timestamp} - {request.remote_addr} - {request.method} - {request.scheme} - {request.full_path} - {response.status}\n<br/>'
    return response


@app.route('/cache', methods=['GET', 'POST'])
@manage_request
def cache():
    return f'hello, this is APP Data: ID={Settings.APP_ID}'


@app.route('/nocache', methods=['GET', 'POST'])
@manage_request
def nocache():
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f'hello, this is non-cached APP. Data: ID={Settings.APP_ID} Time={date}'


@app.route('/protected/ad', methods=['GET', 'POST'])
@manage_request
def protected_ad():
    aduser = request.args.get('aduser')
    adpass = request.args.get('adpass')
    server = Server(Settings.AD_IP_ADDR, get_info=ALL)
    conn = Connection(server, user=aduser, password=adpass, authentication=NTLM)
    if conn.bind():
        return f'hello, this is restricted (by AD) APP Data: ID={Settings.APP_ID} AD_USER={aduser} AD_PASS={adpass}'
    else:
        return f'error code {conn.result["result"]} - hello, AD authentication failed Data: ID={Settings.APP_ID} AD_USER={aduser} AD_PASS={adpass}'


@app.route('/protected/ext', methods=['GET', 'POST'])
@manage_request
def protected_ext():
    return f'hello, this is restricted (by external means) APP Data: ID={Settings.APP_ID}'


@app.route('/db/add', methods=['GET', 'POST'])
@manage_request
def db_add():
    message = request.args.get('message')
    try:
        db_session.add(Messages(message))
        db_session.commit()
        return f'hello, message was saved to DB Data: ID={Settings.APP_ID} Message={message}'
    except:
        return f'sorry, table Messages is non operational or empty Data: ID={Settings.APP_ID} Message={message}'


@app.route('/db/get', methods=['GET', 'POST'])
@manage_request
def db_get():
    try:
        messages = Messages.query.all()
        text = f'hello, these are message from DB Data: ID={Settings.APP_ID}'
        for id, message in enumerate(messages):
            text += f'\n<br/>Message{id}={str(message)}'
        text += '\n'
        return text
    except:
        return f'sorry, table Messages is non operational or empty Data: ID={Settings.PP_ID}'


# @app.route('/fs/add', methods=['GET', 'POST'])
# @manage_request
# def fs_add():
#     filename = f"{Settings.STORAGE_PATH}/myfile.txt"
#     os.makedirs(os.path.dirname(filename), exist_ok=True)
#     with open(filename, "w") as f:
#         f.write("123")
#     return ''


# @app.route('/fs/get', methods=['GET', 'POST'])
# @manage_request
# def fs_get():
#     # return send_from_directory(Settings.STORAGE_PATH, "myfile.txt")
#     return send_file(f"{Settings.STORAGE_PATH}/myfile.txt", as_attachment=True)


@app.route('/bh/set', methods=['GET', 'POST'])
def bh_set():
    global BH_SET
    global BH_CODE
    data = request.values if request.values else request.json
    code = data.get('code')
    try:
        BH_CODE = int(code)
        BH_SET = True
        abort(BH_CODE)
        # return f'Error {BH_CODE}', BH_CODE
    except ValueError:
        return 'NaN'


@app.route('/bh/stop', methods=['GET', 'POST'])
def bh_stop():
    global BH_SET
    BH_SET = False
    return 'Ok'


@app.route('/log/get', methods=['GET', 'POST'])
@manage_request
def log_get():
    global LOG
    return LOG


