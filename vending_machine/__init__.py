from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from vending_machine.config import Config

#app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite///site.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()

def create_app(config_class = Config):
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    from vending_machine.products.routes import products
    app.register_blueprint(products)
    
    return app
