import gc
import json
from flask import current_app, jsonify, request
from flask import Blueprint
from flask_login import login_user

from vending_machine import bcrypt,  db
from vending_machine.models import User

users = Blueprint('users', __name__)

def username_exists(username):
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return True
    else:
        return False

def username_missing(req):
    if 'username' not in req:
        return True
    else:
        return False

def password_missing(req):
    if 'password' not in req:
        return True
    else:
        return False

@users.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        req = request.get_json()
        if username_missing(req):
            return jsonify(message='username not provided')
        if password_missing(req):
            return jsonify(message='password not provided')
        username = req['username']
        password = req['password']
        if username_exists(username):
            return jsonify(message='username already exists. Please register with a different one')
        if 'seller' in req and req['seller'] == True:
            hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, password=hashed_pw, role='seller')
            del hashed_pw
            gc.collect()
        else:
            hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, password=hashed_pw)
            del hashed_pw
            gc.collect()
        with current_app.app_context():
            db.session.add(new_user)
            db.session.commit()
        return jsonify(message = 'registered successfully')
    elif request.method == 'GET':
        return jsonify(
            message = 'Please send email, password and seller (bool) as a post request to /register. '\
                      'Set seller to False if you want to register as a buyer.'
        )

@users.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        req = request.get_json()
        username = req['username']
        password = req['password']
        if not username_exists(username):
            return jsonify(message='login attempt failed due to incorrect username')
        user = User.query.filter_by(username=username).first()
        print(user.password)
        if not bcrypt.check_password_hash(user.password, password):
            return jsonify(message='login attempt failed due to incorrect password')
        elif bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return jsonify(message='login successful')
