from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from vending_machine.config import Config

db = SQLAlchemy()

def create_app(config_class = Config):
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    from vending_machine.products.routes import products
    app.register_blueprint(products)
    
    return app

def init_db(app):
    with app.app_context():
        db.init_app(app)
        return db

