from datetime import datetime
from random import choice
from app import create_app
from models import db, Organization,User
import random

# Create the Flask app
app = create_app()

# Use the app context to interact with the database
with app.app_context():
    # Step 1: Check if tables exist, if not, create them
    db.create_all()

    db.session.commit()

    
    users_data = [
    {"username": "WanjikuK", "email": "wanjiku.kamau@fakemail.com", "password": "wanjikuPass123"},
    {"username": "MwangiJ", "email": "james.mwangi@fakemail.com", "password": "mwangiPass123"},
    {"username": "NyawiraL", "email": "lucy.nyawira@fakemail.com", "password": "nyawiraPass123"},
    {"username": "MutisoD", "email": "david.mutiso@fakemail.com", "password": "mutisoPass123"},
    {"username": "NjeriF", "email": "faith.njeri@fakemail.com", "password": "njeriPass123"},
    {"username": "KaranjaP", "email": "peter.karanja@fakemail.com", "password": "karanjaPass123"},
    {"username": "MuthoniM", "email": "mary.muthoni@fakemail.com", "password": "muthoniPass123"},
    {"username": "KibetC", "email": "charles.kibet@fakemail.com", "password": "kibetPass123"},
    {"username": "ChegeS", "email": "susan.chege@fakemail.com", "password": "chegePass123"},
    {"username": "OmariT", "email": "tom.omari@fakemail.com", "password": "omariPass123"}
]

    def seed_users():
     print("👤 Seeding users...")

     for data in users_data:
        # Check if user already exists to avoid IntegrityError on unique constraint
        existing_user = db.session.query(User).filter_by(email=data['email']).first()
        if not existing_user:
            user = User(
                username=data['username'],
                email=data['email'],
                password=data['password']  # Remember to hash passwords in production
            )
            db.session.add(user)

    # Commit the session to the database
    try:
        db.session.commit()
        print("✅ Users successfully seeded.")
    except Exception as e:
        db.session.rollback()
        print(f"❌ An error occurred: {e}")
    seed_users() 

    organizations_data = [
       {
        "image_url": "https://example.com/images/afyabora.jpg",
        "user_id": random.randint(1, 10),
        "name": "Afya Bora Initiative",
        "description": "Improving healthcare accessibility in underserved communities.",
        "contact_information": "contact@afyabora.org | +254 711 222 333",
        "status": "Active",
        "isAdminApproved": True
    },
    {
        "image_url": "https://example.com/images/techhub.jpg",
        "user_id": random.randint(1, 10),
        "name": "Tech Hub Solutions",
        "description": "Fostering innovation and technology solutions in Mombasa.",
        "contact_information": "info@techhubsolutions.co.ke | +254 722 444 555",
        "status": "Active",
        "isAdminApproved": True
    },
    {
        "image_url": "https://example.com/images/greenagriculture.jpg",
        "user_id": random.randint(1, 10),
        "name": "Green Agriculture",
        "description": "Promoting sustainable agricultural practices in Kisumu.",
        "contact_information": "support@greenagriculture.org | +254 733 555 666",
        "status": "Pending",
        "isAdminApproved": False
    },
    {
        "image_url": "https://example.com/images/youthempowerment.jpg",
        "user_id": random.randint(1, 10),
        "name": "Youth Empowerment Group",
        "description": "Empowering youth through education and vocational training in Machakos.",
        "contact_information": "youth@empowermentgroup.org | +254 744 999 000",
        "status": "Pending",
        "isAdminApproved": False
    },
    {
        "image_url": "https://example.com/images/cleanwaterkenya.jpg",
        "user_id": random.randint(1, 10),
        "name": "Clean Water Kenya",
        "description": "Dedicated to providing clean water solutions to communities in Nakuru.",
        "contact_information": "enquiries@cleanwaterkenya.com | +254 700 111 222",
        "status": "Active",
        "isAdminApproved": True
    },
    {
        "image_url": "https://example.com/images/educationfirst.jpg",
        "user_id": random.randint(1, 10),
        "name": "Education First",
        "description": "Committed to improving education standards in Eldoret through scholarships.",
        "contact_information": "hello@educationfirst.org | +254 711 333 444",
        "status": "Pending",
        "isAdminApproved": False
    },
    {
        "image_url": "https://example.com/images/renewableenergy.jpg",
        "user_id": random.randint(1, 10),
        "name": "Renewable Energy Partners",
        "description": "Advancing renewable energy adoption in Thika for a sustainable future.",
        "contact_information": "contact@renewableenergy.co.ke | +254 722 555 666",
        "status": "Active",
        "isAdminApproved": True
    },
    {
        "image_url": "https://example.com/images/wildlifeconservation.jpg",
        "user_id": random.randint(1, 10),
        "name": "Wildlife Conservation Network",
        "description": "Working to protect endangered species in Garissa and promote biodiversity.",
        "contact_information": "office@wildlifeconservation.net | +254 733 666 777",
        "status": "Pending",
        "isAdminApproved": False
    },
    {
        "image_url": "https://example.com/images/culturalheritage.jpg",
        "user_id": random.randint(1, 10),
        "name": "Cultural Heritage Association",
        "description": "Preserving the rich cultural heritage of Lamu for future generations.",
        "contact_information": "info@culturalheritage.co.ke | +254 720 777 888",
        "status": "Pending",
        "isAdminApproved": False
    },
    {
        "image_url": "https://example.com/images/healthcareforall.jpg",
        "user_id": random.randint(1, 10),
        "name": "Healthcare for All",
        "description": "Ensuring accessible healthcare services for all communities in Meru.",
        "contact_information": "service@healthcareforall.org | +254 750 888 999",
        "status": "Active",
        "isAdminApproved": True
    },
   
]

    for org_data in organizations_data:   
      organization = Organization(
        image_url=org_data["image_url"],
        user_id=org_data["user_id"],
        name=org_data["name"],
        description=org_data["description"],
        contact_information=org_data["contact_information"],
        status=org_data["status"],
        isAdminApproved=org_data["isAdminApproved"]
    )

    db.session.add(organization)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    finally:    
        db.session.close()
