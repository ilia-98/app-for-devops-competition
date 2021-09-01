from werkzeug.utils import redirect

from app import app, Settings, queries, auth_views
from functools import wraps
from datetime import datetime
from flask import request, render_template, jsonify, url_for
from flask_login import login_required

from app.api_views import manage_request
from app.models import Clients, Cars, CarBrands


def api_login(func):
    @wraps(func)
    def wrapper():
        data = request.values if request.values else request.json
        username = data.get('username', None)
        password = data.get('password', None)
        login_values = auth_views.login(username, password)
        if not login_values['logged_in']:
            return jsonify({'error_message': login_values['error_message']})
        return func()
    return wrapper


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/rental')
@login_required
@manage_request
def get_rental_page():
    query = queries.get_rental()
    values = {
        'active_rental': query['active_rental'],
        'finished_rental': query['finished_rental'],
        'active_page': 'rental',
        'external_link': Settings.EXTERNAL_LINK
    }
    return render_template('rental.html', **values)


@app.route('/api/rental', methods=['GET', 'POST'])
@api_login
@manage_request
def api_get_rental():
    query = queries.get_rental()
    active_rental = query['active_rental']
    finished_rental = query['finished_rental']
    values = {
        'active_rental': [i.as_dict() for i in active_rental],
        'finished_rental': [i.as_dict() for i in finished_rental],
        'app_id': Settings.APP_ID,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(values)


@app.route('/rental/add', methods=['GET', 'POST'])
@login_required
@manage_request
def add_rental():
    if request.method == 'GET':
        cars = Cars.query.all()
        if not cars:
            return render_template('modal_error.html', error_message='Нет машин для проката')
        clients = Clients.query.all()
        return render_template('rental_add.html', cars=cars, clients=clients)
    else:
        key, status = queries.add_rental(request.values)
        return jsonify(key=key, status=status)


@app.route('/api/rental/add', methods=['GET', 'POST'])
@api_login
@manage_request
def api_add_rental():
    data = request.values if request.values else request.json
    key, message = queries.add_rental(data)
    values = {
        'field': key,
        'status': message,
        'app_id': Settings.APP_ID,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(values)


@app.route('/rental/finish', methods=['GET', 'POST'])
@login_required
@manage_request
def finish_rental():
    rental_id = request.values.get('id', None)
    queries.finish_rental(rental_id)
    return redirect(url_for('get_rental_page'))


@app.route('/api/rental/finish', methods=['GET', 'POST'])
@api_login
@manage_request
def api_finish_rental():
    data = request.values if request.values else request.json
    rental_id = data.get('id', None)
    message = queries.finish_rental(rental_id)
    values = {
        'status': message,
        'app_id': Settings.APP_ID,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(values)


# @app.route('/employees')
# @login_required
# def get_employees_page():
#     server = Server(Settings.AD_IP_ADDR, get_info=ALL)
#     conn = Connection(server, user=current_user.username, password=current_user.password, authentication=NTLM)
#     conn.search(f'cn=users,{server.info.naming_contexts[0]}', f'(&(objectClass=person)(description=application))', attributes=['*'])
#     return render_template('employees.html', employees=conn.entries, active_page='employees',
#                            page_name='Пользователи', external_link=Settings.EXTERNAL_LINK)


# @app.route('/api/employees', methods=['GET', 'POST'])
# @login_required
# def get_employees():
#     server = Server(Settings.AD_IP_ADDR, get_info=ALL)
#     conn = Connection(server, user=current_user.username, password=current_user.password, authentication=NTLM)
#     if not conn.bind():
#         return jsonify([])
#     conn.search(f'cn=users,{server.info.naming_contexts[0]}', f'(&(objectClass=person)(description=application))', attributes=['*'])
#     users = []
#     for user in conn.entries:
#         users.append(user.name.value)
#     return jsonify(users)


@app.route('/clients')
@manage_request
def get_clients_page():
    clients = queries.get_clients()
    for client in clients:
        client.gender = 'Муж.' if client.gender is True else 'Жен.'
    return render_template('clients.html', clients=clients, active_page='clients',
                           page_name='Клиенты', external_link=Settings.EXTERNAL_LINK)


@app.route('/api/clients', methods=['GET', 'POST'])
@api_login
@manage_request
def get_clients():
    clients = queries.get_clients()
    values = {
        'clients': [i.as_dict() for i in clients],
        'app_id': Settings.APP_ID,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(values)


@app.route('/cars')
@login_required
@manage_request
def get_cars_page():
    cars = queries.get_cars()
    for car in cars:
        car.status = 'Свободна' if car.status is True else 'Занята'
    return render_template('cars.html', cars=cars, active_page='cars', page_name='Машины',
                           external_link=Settings.EXTERNAL_LINK)


@app.route('/api/cars', methods=['GET', 'POST'])
@api_login
@manage_request
def get_cars():
    cars = queries.get_cars()
    values = {
        'cars': [i.as_dict() for i in cars],
        'app_id': Settings.APP_ID,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(values)


@app.route('/cars/add', methods=['GET', 'POST'])
@login_required
@manage_request
def add_car():
    if request.method == 'GET':
        car_brands = CarBrands.query.all()
        return render_template('car_add.html', car_brands=car_brands)
    else:
        key, status = queries.add_car(request.values)
        return jsonify(key=key, status=status)


@app.route('/api/cars/add', methods=['GET', 'POST'])
@api_login
@manage_request
def api_add_car():
    data = request.values if request.values else request.json
    key, message = queries.add_car(data)
    values = {
        'field': key,
        'status': message,
        'app_id': Settings.APP_ID,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(values)

