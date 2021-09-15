### Requirements

Design an API for a vending machine, allowing users with a “seller” role to add, update or remove products, 
while users with a “buyer” role can deposit coins into the machine and make purchases. 
Your vending machine should only accept 5, 10, 20, 50 and 100 cent coins.

### Tasks

- REST API should be implemented consuming and producing “application/json”
- Implement product model with amountAvailable, cost, productName and sellerId fields
- Implement user model with username, password, deposit and role fields
- Implement CRUD for users (POST shouldn’t require authentication)
- Implement CRUD for a product model (GET can be called by anyone, while POST, PUT and DELETE can be called only by the seller user who created the product)
- Implement /deposit endpoint so users with a “buyer” role can deposit 5, 10, 20, 50 and 100 cent coins into their vending machine account
- Implement /buy endpoint (accepts productId, amount of products) so users with a “buyer” role can buy products with the money they’ve deposited. API should return total they’ve spent, products they’ve purchased and their change if there’s any (in 5, 10, 20, 50 and 100 cent coins)
- Implement /reset endpoint so users with a “buyer” role can reset their deposit

### Installation instructions

```bash
git clone https://www.github.com/rohitsrao/vending-machine
cd vending-machine
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
pip install .
```
open vending_machine/config.py and set a value of SECRET_KEY

```bash
python3 run.py
```
