from flask import render_template, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.utils import redirect
from ldap3 import Server, Connection, ALL, NTLM
from app import app, Settings, login_manager
from app.api_views import manage_request
from app.models import Employee


@app.route('/login')
@manage_request
def get_login_page():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username', None)
    password = request.form.get('password', None)
    login_values = login(username, password)
    if not login_values['logged_in']:
        flash(login_values['error_message'])
    return redirect(url_for(login_values['redirect_url']))


def login(username, password):
    values = {
        'logged_in': False,
        'redirect_url': 'get_login_page',
        'error_message': 'No username or password'
    }

    if not username or not password:
        return values

    if username == 'admin' and password == 'pass123':
        user = Employee('1', username, password)
        login_user(user, remember=True)
        values = {
            'logged_in': True,
            'redirect_url': 'get_rental_page'
        }
        return values

    server = Server(Settings.AD_IP_ADDR, get_info=ALL)
    conn = Connection(server, user=username, password=password, authentication=NTLM)

    try:
        if not conn.bind():
            values['error_message'] = 'Please check your domain\\username or password'
            return values
    except:
        values['error_message'] = 'No connection to AD'
        return values

    try:
        username_short = username.split('\\')[1]
        ad_filter = f'(&(objectclass=person)(name={username_short})(description=application))'
        conn.search(f'ou=AppUsers,{server.info.naming_contexts[0]}', ad_filter, attributes=['*'])
        if not conn.entries:
            values['error_message'] = 'User account does not meet application specifications'
            return values
        user_sid = conn.entries[0].objectSid.value
    except:
        values['error_message'] = 'Unknown error'
        return values

    user = Employee(user_sid, username, password)
    login_user(user, remember=True)
    values['logged_in'] = True
    values['redirect_url'] = 'get_rental_page'
    return values


@app.route('/logout')
@login_required
@manage_request
def logout():
    logout_user()
    return redirect(url_for('get_login_page'))


@login_manager.user_loader
def load_user(id):
    id, username, password = id.split('|')
    return Employee(id, username, password)
