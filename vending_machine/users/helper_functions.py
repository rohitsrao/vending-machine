import gc

from flask import current_app
from vending_machine import bcrypt, db
from vending_machine.models import Coinstack, User

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
        total += int(coin[1:]) * req[coin]
    return total

def extract_coin_data(req):
    c5 = req['c5']
    c10 = req['c10']
    c20 = req['c20']
    c50 = req['c50']
    c100 = req['c100']
    return (c5, c10, c20, c50, c100)

def extract_json_request(req):
        username = req['username']
        password = req['password']
        role = req['role']
        return (username, password, role)

def update_coinstack(coinstack, c5, c10, c20, c50, c100):
    coinstack.c5 += c5
    coinstack.c10 += c10
    coinstack.c20 += c20
    coinstack.c50 += c50
    coinstack.c100 += c100
