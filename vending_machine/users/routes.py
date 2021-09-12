import json
from flask import current_app, jsonify, request
from flask import Blueprint

from vending_machine import db
from vending_machine.models import User

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        req = request.get_json()
        username = req['username']
        password = req['password']
        seller = req['seller']
        if seller == True:
            new_user = User(username=username, password=password, role='seller')
        else:
            new_user = User(username=username, password=password)
        with current_app.app_context():
            db.session.add(new_user)
            db.session.commit()
        return jsonify(
            message = 'registered successfully'
        )
    elif request.method == 'GET':
        return jsonify(
            message = 'Please send email, password, confirm_password and seller (bool) as a post request to /register. '\
                      'Set seller to False if you want to register as a buyer.'
        )
