from datetime import datetime
from random import choice
from app import create_app
from models import db, Organization

# Create the Flask app
app = create_app()

# Use the app context to interact with the database
with app.app_context():
    # Step 1: Check if tables exist, if not, create them
    db.create_all()

    db.session.commit()



    print("🏢 Done seeding!")