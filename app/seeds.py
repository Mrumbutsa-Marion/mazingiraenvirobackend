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

    print("🏢 Done seeding!")