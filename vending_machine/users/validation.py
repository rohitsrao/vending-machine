from vending_machine.models import User

def password_missing(req):
    if 'password' not in req: return True
    else: return False

def role_missing(req):
    if 'role' not in req: return True
    else: return False

def username_exists(username):
    existing_user = User.query.filter_by(username=username).first()
    if existing_user: return True
    else: return False

def username_missing(req):
    if 'username' not in req: return True
    else: return False

def validate_register_json_request(req):
    if username_missing(req): return (True, 'username not provided')
    if password_missing(req): return (True, 'password not provided')
    if role_missing(req): return (True, 'role not provided')
    return (False, '')

def validate_username(username):
    if username_exists(username):
        return (True, 'username already exists. Please register with a different one')
    return (False, '')
