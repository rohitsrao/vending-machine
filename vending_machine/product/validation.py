from vending_machine.models import Product

def productName_exists(productName):
    existing_product = Product.query.filter_by(productName=productName).first()
    if existing_product: return True
    else: return False

def validate_productName(productName):
    if productName_exists(productName): return (True, 'productName already exists')
    #if username is None: return (True, 'username cannot be None')
    #if username_exists(username):
    #    return (True, 'username already exists. Please register with a different one')
    #if username_longer_than_20_chars(username): return (True, 'username must be less than 20 characters')
    #if username_contains_space(username): return (True, 'username must not contains spaces')
    return (False, '')
