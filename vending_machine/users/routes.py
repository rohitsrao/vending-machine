import json
from flask import current_app, jsonify, request
from flask import Blueprint

from vending_machine import db
from vending_machine.models import User

users = Blueprint('users', __name__)

def username_already_exists(username):
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
        seller = req['seller']
        if username_already_exists(username):
            return jsonify(message='username already exists. Please register with a different one')
        if seller == True:
            new_user = User(username=username, password=password, role='seller')
        else:
            new_user = User(username=username, password=password)
        with current_app.app_context():
            db.session.add(new_user)
            db.session.commit()
        return jsonify(message = 'registered successfully')
    elif request.method == 'GET':
        return jsonify(
            message = 'Please send email, password and seller (bool) as a post request to /register. '\
                      'Set seller to False if you want to register as a buyer.'
        )
