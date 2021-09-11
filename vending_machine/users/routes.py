from flask import jsonify
from flask import Blueprint

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET'])
def home():
    return jsonify(
        message = 'Please send email, password, confirm_password as a post request to /register'
    )
