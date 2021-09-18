from vending_machine.models import Product

def amount_available_greater_than_15(amountAvailable):
    if amountAvailable > 15: return True
    else: return False

def productName_exists(productName):
    existing_product = Product.query.filter_by(productName=productName).first()
    if existing_product: return True
    else: return False

def productName_longer_than_32_characters(productName):
    if len(productName) > 32: return True
    else: return False

def validate_amountAvailable(amountAvailable):
    if amount_available_greater_than_15: return (True, 'amountAvailable must be lesser than or equal to 15')
    return (False, '')

def validate_productName_when_adding_product(productName):
    if productName is None: return (True, 'productName cannot be None')
    if productName_exists(productName): return (True, 'productName already exists')
    if productName_longer_than_32_characters(productName): return (True, 'productName must be shorter than 32 characters')
    return (False, '')

def validate_productName_during_update(productName):
    if productName is None: return (True, 'productName cannot be None')
    if productName_longer_than_32_characters(productName): return (True, 'productName must be shorter than 32 characters')
    return (False, '')
