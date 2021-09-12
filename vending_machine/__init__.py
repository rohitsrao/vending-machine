from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from vending_machine.config import Config

bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class = Config):
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    from vending_machine.products.routes import products
    from vending_machine.users.routes import users
    app.register_blueprint(products)
    app.register_blueprint(users, url_prefix='/user')
    
    with app.app_context():
        bcrypt.init_app(app)
        db = init_db(app)
        db.create_all()
        login_manager.init_app(app)
    
    return app

def init_db(app):
    with app.app_context():
        db.init_app(app)
        return db
