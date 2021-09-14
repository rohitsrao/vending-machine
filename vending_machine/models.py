from flask_login import UserMixin
from vending_machine import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    deposit = db.Column(db.Float, default=0.0)
    role = db.Column(db.String(6), default='buyer')
    products_sold = db.relationship('Product', backref='seller')
     
    def __repr__(self):
        return f"User('{self.username}', {self.deposit}, '{self.role}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(128))
    amountAvailable = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    sellerId = db.Column(db.Integer, db.ForeignKey('user.id'))
     
    def __repr__(self):
        return f"Product('{self.productName}', {self.amountAvailable}, {self.cost}, {self.sellerId})"

class Coinstack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    c5 = db.Column(db.Integer, default=40, nullable=False)
    c10 = db.Column(db.Integer, default=40, nullable=False)
    c20 = db.Column(db.Integer, default=40, nullable=False)
    c50 = db.Column(db.Integer, default=40, nullable=False)
    c100 = db.Column(db.Integer, default=40, nullable=False)
    
    def __repr__(self):
        return f"Coinstack(5c: '{self.c5}', 10c: '{self.c10}', 20c: '{self.c20}', 50c: '{self.c50}', 100c: '{self.c100}')"

