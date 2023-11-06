from datetime import datetime
from random import choice
from app import create_app
from models import db, Organization,User,Donation,Beneficiary,Inventory
from datetime import datetime, timedelta
import random
import string

# Create the Flask app
app = create_app()

# Use the app context to interact with the database
with app.app_context():
    # Step 1: Check if tables exist, if not, create them
    db.create_all()

    db.session.commit()

    # Step 3: Seeding organizations
    print("🏢 Seeding organizations...")
    organizations_data = [
          {
        "image_url": "https://img.freepik.com/free-photo/green-field-tree-blue-skygreat-as-backgroundweb-banner-generative-ai_1258-152184.jpg?size=626&ext=jpg&ga=GA1.1.471148710.1698917037&semt=ais",
        "name": "Green Horizons",
        "description": "Green Horizons is at the forefront of urban reforestation, engaging communities in planting trees to restore natural habitats and reduce the urban heat island effect. Our initiatives support biodiversity and provide educational programs on the importance of urban greenery for future generations. Join us in creating greener and healthier cities!",
        "contact_information": "info@greenhorizons.org",
        "status": "Active",
        "isAdminApproved": True
    },
    {
        "image_url": "https://img.freepik.com/free-photo/pollution-concept-water-with-garbage_23-2149094962.jpg?w=1380&t=st=1698917787~exp=1698918387~hmac=cf2f576d666826f85d15d2c24216f42a2daddaf1179f845843212403a9fdbfb1",
        "name": "Blue Planet Protectors",
        "description": "With a mission to safeguard oceanic ecosystems, Blue Planet Protectors leads cleanup drives to remove plastic pollution from our seas. Our marine conservation efforts also involve the protection of coral reefs through the cultivation of coral fragments and the promotion of sustainable fishing practices. Together, let's protect our blue planet for future generations!",
        "contact_information": "contact@blueplanetprotectors.org",
        "status": "Pending",
        "isAdminApproved": False
    },
    {
        "image_url": "https://img.freepik.com/free-photo/close-up-community-concept-with-hands_23-2148931127.jpg?w=1380&t=st=1698933938~exp=1698934538~hmac=423be1d6262928f63458364dd187a8cfb41f0a04a7063c9e2fbf09c8b686ee59",
        "name": "Eco Warriors",
        "description": "Eco Warriors is a grassroots movement promoting sustainable living through community workshops, green energy projects, and zero-waste challenges. We partner with local schools and businesses to implement eco-friendly initiatives that make sustainability an accessible goal for everyone. Join us and become an eco-warrior for a better future!",
        "contact_information": "support@ecowarriors.org",
        "status": "Active",
        "isAdminApproved": True
    },
    {
        "image_url": "https://img.freepik.com/free-photo/amazing-bengal-tiger-nature-with-gazelles_475641-1195.jpg?w=1380&t=st=1698934044~exp=1698934644~hmac=15e04b14594b41b9c4e21c758134b0309b7b0e1c7ceb3b036e024e1d29c6cfdc",
        "name": "Wildlife Guardians",
        "description": "Dedicated to the protection of endangered wildlife, our organization conducts research, supports anti-poaching patrols, and runs rehabilitation centers for injured animals. Wildlife Guardians works globally to ensure that future generations will enjoy a world teeming with biodiversity. Join us in safeguarding our precious wildlife!",
        "contact_information": "help@wildlifeguardians.org",
        "status": "Inactive",
        "isAdminApproved": True
    },
    {
        "image_url": "https://img.freepik.com/free-photo/hands-plant-young-green-sprout-tree-three-volunteers_1157-50576.jpg?w=1380&t=st=1698934131~exp=1698934731~hmac=e88b94634654c66354ff5c5f54a593383514cc6c67a527953396cd2fe90a71de",
        "name": "Forest Renewal Alliance",
        "description": "The Forest Renewal Alliance is an international advocate for the world's forests, focusing on reversing the damage done by deforestation and promoting sustainable forestry practices. Our reforestation projects have planted millions of trees, with a focus on species diversity to ensure resilient ecosystems. Join us in restoring and preserving our forested lands!",
        "contact_information": "outreach@forestalliance.org",
        "status": "Active",
        "isAdminApproved": False
    },
    {
        "image_url": "https://img.freepik.com/free-photo/exterior-portrait-kids-world-environment-day_23-2149369441.jpg?w=1380&t=st=1698934214~exp=1698934814~hmac=0b5b2f16c5266994ebb4e467ea85aa0490366415429b2840815e4e9f192d9859",
        "name": "Climate Action Network",
        "description": "The Climate Action Network is a coalition of individuals and organizations working tirelessly to shape public policy and raise awareness about climate change. We lobby for aggressive carbon reduction targets, support renewable energy adoption, and help communities adapt to climate impacts. Join us and take action against climate change!",
        "contact_information": "info@climateaction.net",
        "status": "Under Review",
        "isAdminApproved": False
    },
    {
        "image_url": "https://img.freepik.com/free-photo/new-life-begins-with-one-person-care-generated-by-ai_188544-45400.jpg?t=st=1698917334~exp=1698920934~hmac=d4b843bce506ecb93468b493266a6b697d2f9a6da0fead29adba0b51fa3a6eba&w=1480",
        "name": "Sustainable Futures Foundation",
        "description": "Sustainable Futures Foundation champions the development and implementation of cutting-edge renewable energy solutions. We collaborate with technologists, scientists, and policymakers to create a roadmap for a sustainable energy future, minimizing our collective carbon footprint. Join us in building a sustainable future!",
        "contact_information": "contact@sustainablefutures.org",
        "status": "Active",
        "isAdminApproved": True
    },
    {
        "image_url": "https://img.freepik.com/free-photo/group-happy-african-volunteers-hold-blank-board-with-faith-sign-park-africa-volunteering-charity-people-ecology-concept_627829-322.jpg?w=1380&t=st=1698934389~exp=1698934989~hmac=1c2df6189a2401929fb2fb48ece4cc348149cf16b2eedeff8072e8cee68e71fc",
        "name": "Eco Education Outreach",
        "description": "Through our comprehensive environmental education programs, Eco Education Outreach aims to inspire a new generation of eco-conscious citizens. We offer hands-on learning experiences, sustainability-focused curriculum resources, and community service projects that promote environmental stewardship. Join us in empowering the next generation of environmental leaders!",
        "contact_information": "outreach@ecoeducation.org",
        "status": "Pending",
        "isAdminApproved": True
    },
      {
        "image_url": "https://img.freepik.com/free-photo/closeup-shot-elephants-standing-near-lake-sunset_181624-29375.jpg?w=1380&t=st=1698934754~exp=1698935354~hmac=aa50069cb02a8491cb12047620b0d49a31b9a3f2f73e7df74161d00de83766b9",
        "name": "Biodiversity Preservation Society",
        "description": "The Biodiversity Preservation Society is a global force for the protection of all forms of life on Earth. Our conservation projects range from safeguarding natural habitats to legislative advocacy for wildlife corridors and biodiversity hotspots, ensuring nature's balance is maintained.",
        "contact_information": "preserve@biodiversitysociety.org",
        "status": "Active",
        "isAdminApproved": False
    },
    {
        "image_url": "https://img.freepik.com/free-photo/close-up-man-writing-notebook_23-2148894050.jpg?w=1380&t=st=1698934812~exp=1698935412~hmac=8210a62801c5a93b0acdd305b60f52d8441d1f1a59045256c4e668c68a948f61",
        "name": "Urban Greening Initiative",
        "description": "Urban Greening Initiative's goal is to transform concrete jungles into lush, green landscapes. Our projects create parks and green roofs, and promote urban agriculture to enhance food security, improve air quality, and provide serene green spaces for all city dwellers to enjoy.",
        "contact_information": "urban.greening@initiative.org",
        "status": "Suspended",
        "isAdminApproved": True
    
    },

 
  
    ]

    for data in organizations_data:
        organization = Organization(**data)
        db.session.add(organization)

    db.session.commit()

   
 
    users_data = [

    {"username": "KinyuaA", "email": "alice.kinyua@fakemail.com", "password": "kinyuaSecure1!"},
    {"username": "OtienoZ", "email": "zachary.otieno@fakemail.com", "password": "otienoZee123!"},
    {"username": "KipronoE", "email": "esther.kiprono@fakemail.com", "password": "kipronoPass789!"},
    {"username": "OdhiamboR", "email": "ruth.odhiambo@fakemail.com", "password": "odhiamboRuth!456"},
    {"username": "MainaS", "email": "simon.maina@fakemail.com", "password": "mainaS3cur3!"},
    {"username": "OchiengD", "email": "diana.ochieng@fakemail.com", "password": "ochiengPass!321"},
    {"username": "KimathiJ", "email": "julius.kimathi@fakemail.com", "password": "kimathiJ254!!"},
    {"username": "WambuiG", "email": "grace.wambui@fakemail.com", "password": "wambuiG!Password"},
    {"username": "MbogoL", "email": "lucas.mbogo@fakemail.com", "password": "lucasMbogo123!"},
    {"username": "OkothP", "email": "paul.okoth@fakemail.com", "password": "okothPaul!987"}



]

    for data in users_data:
         existing_user = User.query.filter((User.username == data['username']) | (User.email == data['email'])).first()
         if not existing_user:
           user = User(**data)
           db.session.add(user)

    db.session.commit()

def seed_donations():
    donations_data = [
    {
        "donor_user_id": 1,
        "organization_id": 1,
        "amount": 2500.00,
        "donation_type": "One-time",
        "anonymous": False,
        "date": "2023-10-01",
        "transaction_id": "TXN12345"
    },
    {
        "donor_user_id": 2,
        "organization_id": 2,
        "amount": 1500.00,
        "donation_type": "Monthly",
        "anonymous": True,
        "date": "2023-10-02",
        "transaction_id": "TXN12346"
    },
    {
        "donor_user_id": 3,
        "organization_id": 3,
        "amount": 3000.00,
        "donation_type": "Annual",
        "anonymous": False,
        "date": "2023-10-03",
        "transaction_id": "TXN12347"
    },
    {
        "donor_user_id": 4,
        "organization_id": 4,
        "amount": 5000.00,
        "donation_type": "One-time",
        "anonymous": True,
        "date": "2023-10-04",
        "transaction_id": "TXN12348"
    },
    {
        "donor_user_id": 5,
        "organization_id": 5,
        "amount": 7000.00,
        "donation_type": "Monthly",
        "anonymous": False,
        "date": "2023-10-05",
        "transaction_id": "TXN12349"
    },

    {
        "donor_user_id": 6,
        "organization_id": 6,
        "amount": 7050.00,
        "donation_type": "Monthly",
        "anonymous": False,
        "date": "2023-10-06",
        "transaction_id": "TXN12350"
    },
    {
        "donor_user_id": 7,
        "organization_id": 7,
        "amount": 7600.00,
        "donation_type": "Monthly",
        "anonymous": False,
        "date": "2023-10-05",
        "transaction_id": "TXN12351"
    },
    {
        "donor_user_id": 8,
        "organization_id": 8,
        "amount": 850.00,
        "donation_type": "Monthly",
        "anonymous": False,
        "date": "2023-10-05",
        "transaction_id": "TXN12352"
    },
    {
        "donor_user_id": 9,
        "organization_id": 9,
        "amount": 7590.00,
        "donation_type": "Monthly",
        "anonymous": False,
        "date": "2023-10-05",
        "transaction_id": "TXN12353"
    },
    {
        "donor_user_id": 10,
        "organization_id":10,
        "amount": 750.00,
        "donation_type": "Monthly",
        "anonymous": False,
        "date": "2023-10-05",
        "transaction_id": "TXN12354"
    },
]

def seed_donations():
    print("💰 Seeding donations...")

    user_ids = [user.id for user in User.query.all()]
    organization_ids = [organization.id for organization in Organization.query.all()]

    donations_data = [
        {
            "donor_user_id": choice(user_ids),
            "organization_id": choice(organization_ids),
            "amount": random.uniform(50.0, 5000.0),  
            "donation_type": choice(["One-time", "Monthly", "Annual"]),
            "anonymous": choice([True, False]),
            "date": datetime.utcnow() - timedelta(days=random.randint(0, 365)),
            "transaction_id": f"TXN{random.randint(100000, 999999)}"
        } for _ in range(20)  
    ]

    for data in donations_data:
        donation = Donation(**data)
        db.session.add(donation)

    db.session.commit()


with app.app_context():
    seed_donations()

# kenyan_names = [
#     "Wanjiru Muthoni", "Kamau Njoroge", "Mwangi Kimani", "Njeri Wangari",
#     "Wambui Waweru", "Gachoka Muturi", "Nyawira Maina", "Makena Njeru",
#     "Onyango Otieno", "Atieno Akoth", "Akinyi Omondi", "Adhiambo Omollo",
#     "Otieno Owuor", "Ochieng Okoth", "Kipchoge Keino", "Chebet Kosgei",
#     "Kiplagat Bett", "Tanui Cheruiyot", "Cheruiyot Barasa", "Maritim Kigen"
# ]

# descriptions = [
#     "A local farmer who contributes to community agriculture programs.",
#     "A talented artist who teaches painting to children in the community.",
#     "A single mother of three who actively participates in local self-help groups.",
#     "A dedicated teacher who has been providing free education to underprivileged children.",
#     "A community health worker who has been instrumental in local vaccination drives.",
#     "An entrepreneur who has started a small business with the help of community loans.",
#     "A young athlete training for national competitions with hopes of representing Kenya.",
#     "A skilled carpenter providing affordable furniture to local schools and hospitals."
# ]

# inventory_received_examples = [
#     "5 bags of maize, 10 kgs of beans, 2 blankets",
#     "Art supplies including paints, brushes, and canvases",
#     "Monthly food ration, school supplies for the children",
#     "Books, desks, and learning materials for the classroom",
#     "Medical kits, gloves, and face masks for health campaigns",
#     "Seed capital fund, business training manuals",
#     "Sports gear, running shoes, and athletic clothing",
#     "Woodworking tools, safety equipment, and varnish"
# ]

# def clear_beneficiaries():
#     try:
#         num_rows_deleted = db.session.query(Beneficiary).delete()
#         db.session.commit()
#         print(f"Cleared {num_rows_deleted} rows from Beneficiary table.")
#     except Exception as e:
#         print(f"Error clearing Beneficiary table: {e}")
#         db.session.rollback()

# def seed_beneficiaries(num):
#     for _ in range(num):
#         name = random.choice(kenyan_names)
#         description = random.choice(descriptions)
#         inventory_received = random.choice(inventory_received_examples)
#         new_beneficiary = Beneficiary(name=name, description=description, inventory_received=inventory_received)
#         db.session.add(new_beneficiary)
#     db.session.commit()    

# app = create_app()
# with app.app_context():
#     db.init_app(app)
#     db.create_all()
#     clear_beneficiaries()
#     seed_beneficiaries(50)
def seed_beneficiaries():
    print("👥 Seeding beneficiaries...")


    try:
        num_rows_deleted = db.session.query(Beneficiary).delete()
        db.session.commit()
        print(f"Cleared {num_rows_deleted} rows from Beneficiary table.")
    except Exception as e:
        print("An error occurred while clearing the Beneficiary table:", e)
        db.session.rollback()
        return 

    beneficiaries_data = [
     {
        "organization_id": 1,  
        "name": "Green Horizons",
        "description": "Advocates for reforestation in deforested regions of Kenya.",
        "inventory_received": "Seedlings, Gardening Tools, Watering Cans",
     },
     {
        "organization_id": 2,
        "name": "Clean Oceans Kenya",
        "description": "Focused on cleaning up Kenya's coastline and promoting recycling of ocean waste.",
        "inventory_received": "Recycling Bins, Trash Bags, Protective Gloves",
     },
     {
        "organization_id": 3,
        "name": "Savannah Protectors",
        "description": "Works to prevent illegal poaching and protect wildlife habitats.",
        "inventory_received": "Binoculars, GPS Devices, Ranger Gear",
     },
     {
        "organization_id": 4,
        "name": "Kenya Climate Champions",
        "description": "Educates communities on climate change impacts and sustainable living.",
        "inventory_received": "Educational Materials, Solar Lamps, Tree Seedlings",
     },
     {
        "organization_id": 5,
        "name": "Eco Warriors Trust",
        "description": "Empowers youth to participate in environmental conservation projects.",
        "inventory_received": "Workbooks, Educational Kits, Reusable Water Bottles",
     },
     {
        "organization_id": 6,
        "name": "Urban Green Spaces",
        "description": "Creates and maintains green spaces in urban areas of Kenya.",
        "inventory_received": "Gardening Equipment, Seeds, Soil Fertilizers",
     },
     {
        "organization_id": 7,
        "name": "Renewable Energy for Kenya",
        "description": "Promotes the use of renewable energy sources within local communities.",
        "inventory_received": "Solar Panels, Wind Turbines, Installation Kits",
     },
     {
        "organization_id": 8,
        "name": "Water Conservation Coalition",
        "description": "Aims to preserve Kenya's freshwater resources through conservation efforts.",
        "inventory_received": "Water Tanks, Irrigation Systems, Water Filters",
     },
     {
        "organization_id": 9,
        "name": "Waste Not Kenya",
        "description": "Advocates for zero waste lifestyles and provides composting solutions.",
        "inventory_received": "Compost Bins, Educational Pamphlets, Reusable Bags",
     },
     {
        "organization_id": 10,
        "name": "Forest Guardians",
        "description": "Engages in the protection and expansion of Kenya's forest cover.",
        "inventory_received": "Tree Seedlings, Reforestation Guides, Ecological Monitoring Tools",
     }
  ]

    for data in beneficiaries_data:
        beneficiary = Beneficiary(
            organization_id=data["organization_id"],
            name=data["name"],
            description=data["description"],
            inventory_received=data["inventory_received"]
        )
        db.session.add(beneficiary)

    try:
        db.session.commit()
    except Exception as e:
        print("An error occurred while seeding the Beneficiary table:", e)
        db.session.rollback()

with app.app_context(): 
    db.create_all()   
    seed_beneficiaries()       


def seed_inventory():
    environmental_inventory = [
        Inventory(beneficiary_id=1, description='Tree saplings for reforestation', quantity=100, date_received=datetime.utcnow()),
        Inventory(beneficiary_id=1, description='Gardening tools for community garden', quantity=10, date_received=datetime.utcnow()),
        Inventory(beneficiary_id=2, description='Recycling bins for plastic waste', quantity=50, date_received=datetime.utcnow()),
        Inventory(beneficiary_id=2, description='Composting kits for organic waste', quantity=30, date_received=datetime.utcnow()),
        Inventory(beneficiary_id=3, description='Water testing kits for river clean-up', quantity=15, date_received=datetime.utcnow()),
        Inventory(beneficiary_id=3, description='Reusable bags for litter collection', quantity=200, date_received=datetime.utcnow()),
        Inventory(beneficiary_id=4, description='Biodegradable planting pots', quantity=500, date_received=datetime.utcnow()),
        Inventory(beneficiary_id=4, description='Solar-powered outdoor lights', quantity=25, date_received=datetime.utcnow()),
        Inventory(beneficiary_id=5, description='Educational materials on recycling', quantity=1000, date_received=datetime.utcnow()),
        Inventory(beneficiary_id=5, description='Wildlife tracking collars for research', quantity=5, date_received=datetime.utcnow()),
    ]
    with app.app_context():
     db.session.bulk_save_objects(environmental_inventory)

     try:
        db.session.commit()
        print('Environmental inventory seeded successfully.')
     except Exception as e:
        db.session.rollback()
        print('An error occurred while seeding environmental inventory:', str(e))
seed_inventory()


print("🏢 Done seeding!")