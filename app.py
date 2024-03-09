import json
import os
from functools import wraps

from flask import Flask, redirect, url_for
from flask import jsonify, render_template, request

app = Flask(__name__)
# Utilisateurs autorisés (vous pouvez remplacer cela par une base de données utilisateur)
AUTHORIZED_USERS = {'sadish': 'sadish1'}


@app.route('/')
def index():
    return redirect(url_for('login'))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in request.cookies or 'password' not in request.cookies:
            return redirect(url_for('login'))
        elif request.cookies['username'] not in AUTHORIZED_USERS or request.cookies['password'] != AUTHORIZED_USERS[
            request.cookies['username']]:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in AUTHORIZED_USERS and password == AUTHORIZED_USERS[username]:
            response = redirect(url_for('results'))
            response.set_cookie('username', username)
            response.set_cookie('password', password)
            return response
    return render_template('login.html')


@app.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    data_folder = os.path.join(os.path.dirname(__file__), 'data')  # Chemin 'os'
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    files = [f for f in os.listdir(data_folder) if f.endswith('.json')]
    selected_file = request.form.get('selected_file')

    if selected_file:
        file_path = os.path.join(data_folder, selected_file)
        with open(file_path, 'r') as file:
            results = json.load(file)
    else:
        results = None

    return render_template('results.html', files=files, results=results)


@app.route('/check-update', methods=['GET'])
@login_required
def check_update():
    data_folder = os.path.join(os.path.dirname(__file__), 'data')
    most_recent_file = max([os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith('.json')],
                           default=None, key=os.path.getmtime)
    if most_recent_file:
        return jsonify({"update": True, "file": os.path.basename(most_recent_file),
                        "timestamp": os.path.getmtime(most_recent_file)})
    return jsonify({"update": False})


@app.route('/logout')
def logout():
    response = redirect(url_for('login'))
    response.delete_cookie('username')
    response.delete_cookie('password')
    return response


if __name__ == '__main__':
    app.run(debug=True)
