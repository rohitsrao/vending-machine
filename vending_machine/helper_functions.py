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

def coin_change_calculator(change_amount, num_coins_available):
    coins = ['c100', 'c50', 'c20', 'c10', 'c5']
    values = [100, 50, 20, 10, 5]
    for i in range(len(coins)):
        change_coins = {'c5': 0, 'c10': 0, 'c20': 0, 'c50': 0, 'c100': 0} 
        tmp = change_amount
        coin_list = coins[i:]
        value_list = values[i:]
        for j in range(len(coin_list)):
            coin = coin_list[j]
            value = value_list[j]
            for k in range(num_coins_available[coin]):
                if (change_coins[coin]+1) * value <= tmp:
                    change_coins[coin] += 1
            tmp -= change_coins[coin] * value
        total = 0
        for coin in coin_list:
            total += change_coins[coin] * int(str(coin[1:]))
        if total == change_amount:
            return change_coins

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

def format_num_coins_available(coinstack):
    num_coins_available = {
        'c5': coinstack.c5,
        'c10': coinstack.c10,
        'c20': coinstack.c20,
        'c50': coinstack.c50,
        'c100': coinstack.c100
    }
    return num_coins_available

def update_coinstack(coinstack, c5, c10, c20, c50, c100):
    coinstack.c5 += c5
    coinstack.c10 += c10
    coinstack.c20 += c20
    coinstack.c50 += c50
    coinstack.c100 += c100
