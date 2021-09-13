import gc

from flask import current_app
from vending_machine import bcrypt, db
from vending_machine.models import User

def add_new_user_to_db(username, password, role):
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_pw, role=role)
    del hashed_pw
    gc.collect()
    with current_app.app_context():
        db.session.add(new_user)
        db.session.commit()

def compute_total_deposit(req):
    total = 0
    for coin in req:
        total += int(coin) * req[coin]
    return total

def extract_json_request(req):
        username = req['username']
        password = req['password']
        role = req['role']
        return (username, password, role)

