import gc
import json
from flask import current_app, jsonify, request
from flask import Blueprint
from flask_login import current_user, login_user, logout_user

from vending_machine import bcrypt,  db
from vending_machine.models import User

users = Blueprint('users', __name__)

def add_new_user_to_db(username, password, role):
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_pw, role=role)
    del hashed_pw
    gc.collect()
    with current_app.app_context():
        db.session.add(new_user)
        db.session.commit()

def extract_json_request(req):
        username = req['username']
        password = req['password']
        role = req['role']
        return (username, password, role)

def password_missing(req):
    if 'password' not in req: return True
    else: return False

def role_missing(req):
    if 'role' not in req: return True
    else: return False

def username_exists(username):
    existing_user = User.query.filter_by(username=username).first()
    if existing_user: return True
    else: return False

def username_missing(req):
    if 'username' not in req: return True
    else: return False

def validate_register_json_request(req):
    if username_missing(req): return (True, 'username not provided')
    if password_missing(req): return (True, 'password not provided')
    if role_missing(req): return (True, 'role not provided')
    return (False, '')

def validate_username(username):
    if username_exists(username):
        return (True, 'username already exists. Please register with a different one')
    return (False, '')

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return jsonify(message='user already logged in')
    if request.method == 'POST':
        req = request.get_json()
        register_json_is_invalid, error_message = validate_register_json_request(req)
        if register_json_is_invalid: return jsonify(message=error_message)
        username, password, role = extract_json_request(req)
        username_is_invalid, error_message = validate_username(username)
        if username_is_invalid: return jsonify(message=error_message)
        if role == 'seller':
            add_new_user_to_db(username, password, 'seller')
        else:
            add_new_user_to_db(username, password, 'buyer')
        return jsonify(message = 'registered successfully')
    elif request.method == 'GET':
        return jsonify(
            message = 'Please send email, password and seller (bool) as a post request to /register. '\
                      'Set seller to False if you want to register as a buyer.'
        )

@users.route('/account', methods=['GET'])
def account():
    if current_user.is_authenticated:
        return jsonify(
            username = current_user.username,
            deposit = current_user.deposit,
            role = current_user.role
        )
    else:
        return jsonify(message='user must be logged in to access this page')

@users.route('/account/update_username', methods=['PATCH'])
def update_username():
    if current_user.is_authenticated:
        req = request.get_json()
        new_username = req['username']
        if username_exists(new_username):
            return jsonify(message='new username already exists. Please choose a different one.')
        user = User.query.filter_by(username=current_user.username).first()
        user.username = new_username
        db.session.commit()
        return jsonify(message='username updated')
    else:
        return jsonify(message='user must be logged in to update username')

@users.route('/account/update_password', methods=['PATCH'])
def update_password():
    if current_user.is_authenticated:
        req = request.get_json()
        new_password = req['password']
        hashed_pw = bcrypt.generate_password_hash(new_password).decode('utf-8')
        user = User.query.filter_by(username=current_user.username).first()
        user.password = hashed_pw
        db.session.commit()
        del hashed_pw
        gc.collect()
        return jsonify(message='password updated')
    else: 
        return jsonify(message='user must be logged in to update password')

@users.route('/account/delete', methods=['DELETE'])
def delete_account():
    if current_user.is_authenticated:
        req = request.get_json()
        password = req['password']
        if password == None:
            return jsonify(message='Null password received. Account cannot be deleted without password confirmation.')
        elif password == '':
            return jsonify(message='Empty password received. Account cannot be deleted without password confirmation.')
        elif not bcrypt.check_password_hash(current_user.password, password):
            return jsonify(message='password incorrect. Please check and try again')
        else:
            user = User.query.filter_by(username=current_user.username).first()
            with current_app.app_context():
                db.session.delete(user)
                db.session.commit()
            return jsonify(message='user account deleted')
    else:
        return jsonify(message='user must be logged in to delete account')

@users.route('/account/update_role', methods=['PATCH'])
def update_role():
    if current_user.is_authenticated:
        req = request.get_json()
        new_role = req['role']
        user = User.query.filter_by(username=current_user.username).first()
        user.role = new_role
        db.session.commit()
        return jsonify(message='role updated')
    else:
        return jsonify(message='user must be logged in to update role')

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return jsonify(message='user already logged in')
    if request.method == 'POST':
        req = request.get_json()
        username = req['username']
        password = req['password']
        if not username_exists(username):
            return jsonify(message='login attempt failed due to incorrect username')
        user = User.query.filter_by(username=username).first()
        if not bcrypt.check_password_hash(user.password, password):
            return jsonify(message='login attempt failed due to incorrect password')
        elif bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return jsonify(message='login successful')
    elif request.method == 'GET':
        return jsonify(message='please make valid post request with username and password')

@users.route('/logout', methods=['GET'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify(message='user logged out successfully')
    else: 
        return jsonify(message='user not logged in')
