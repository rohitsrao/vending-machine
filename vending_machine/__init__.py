from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from vending_machine.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(config_class = Config):
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    from vending_machine.products.routes import products
    from vending_machine.users.routes import users
    app.register_blueprint(products)
    app.register_blueprint(users, url_prefix='/user')
    
    db = init_db(app)
    with app.app_context():
        db.create_all()
        bcrypt.init_app(app)
    
    return app

def init_db(app):
    with app.app_context():
        db.init_app(app)
        return db
