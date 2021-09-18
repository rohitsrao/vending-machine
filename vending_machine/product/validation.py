from vending_machine.models import Product

def productName_exists(productName):
    existing_product = Product.query.filter_by(productName=productName).first()
    if existing_product: return True
    else: return False

def productName_longer_than_32_characters(productName):
    if len(productName) > 32: return True
    else: return False

def validate_productName(productName):
    if productName is None: return (True, 'productName cannot be None')
    if productName_exists(productName): return (True, 'productName already exists')
    if productName_longer_than_32_characters(productName): return (True, 'productName must be shorter than 32 characters')
    #if username is None: return (True, 'username cannot be None')
    #if username_exists(username):
    #    return (True, 'username already exists. Please register with a different one')
    return (False, '')
