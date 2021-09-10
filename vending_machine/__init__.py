from flask import Flask

app = Flask(__name__)

from vending_machine import routes
