from vending_machine.models import User

def password_is_shorter_than_8_chars(password):
    if len(password) < 8: return True
    else: return False

def password_missing(req):
    if 'password' not in req: return True
    else: return False

def password_same_as_username(password, username):
    if password == username: return True
    else: return False

def role_missing(req):
    if 'role' not in req: return True
    else: return False

def username_contains_space(username):
    if ' ' in username: return True
    else: return False

def username_exists(username):
    existing_user = User.query.filter_by(username=username).first()
    if existing_user: return True
    else: return False

def username_longer_than_20_chars(username):
    if len(username) > 20: return True
    else: return False

def username_missing(req):
    if 'username' not in req: return True
    else: return False

def validate_password(password, username):
    if password is None: return(True, 'password cannot be None')
    if password_is_shorter_than_8_chars(password): return (True, 'password must be longer than 8 characters')
    if password_same_as_username(password, username): return (True, 'password cannot be same as username')
    return (False, '')

def validate_register_json_request(req):
    if username_missing(req): return (True, 'username not provided')
    if password_missing(req): return (True, 'password not provided')
    if role_missing(req): return (True, 'role not provided')
    return (False, '')

def validate_username(username):
    if username is None: return (True, 'username cannot be None')
    if username_exists(username):
        return (True, 'username already exists. Please register with a different one')
    if username_longer_than_20_chars(username): return (True, 'username must be less than 20 characters')
    if username_contains_space(username): return (True, 'username must not contains spaces')
    return (False, '')
