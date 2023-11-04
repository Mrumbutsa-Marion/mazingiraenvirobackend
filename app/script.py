from random import choice
from models import db, Beneficiary,Payment
from app import app
import time

kenyan_names = ["John", "Jane", "David", "Linda"]
descriptions = ["Description 1", "Description 2", "Description 3"]
inventory_received_examples = ["Item A", "Item B", "Item C"]

def seed_beneficiaries(num):
    with app.app_context():
        for _ in range(num):
            name = choice(kenyan_names)
            description = choice(descriptions)
            inventory_received = choice(inventory_received_examples)
            new_beneficiary = Beneficiary(name=name, description=description, inventory_received=inventory_received)
            db.session.add(new_beneficiary)
        db.session.commit()

# Call the seed_beneficiaries function to add a new beneficiary
seed_beneficiaries(1)
# Use the app context to interact with the database

