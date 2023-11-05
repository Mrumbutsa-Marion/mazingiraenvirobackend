from datetime import datetime
from random import choice,random
from datetime import timedelta
from app import create_app
from models import db, Organization ,User,Inventory,Beneficiary,Donation,Payment,Story,Reminder


      # Create the Flask app
app = create_app()

    
with app.app_context():
    print("📖 Seeding stories...")
    stories_data = [
        {
            "organization_id": 1,
            "title": "Helping Underprivileged Children",
            "content": "We organized a charity event to provide education and support to underprivileged children in our community. Thanks to the generous donations from our supporters, we were able to make a positive impact on their lives.",
            "images": "https://example.com/images/story1.jpg",
            "date_created": datetime.utcnow()
        },
        {
            "organization_id": 2,
            "title": "Supporting Local Farmers",
            "content": "We partnered with local farmers to promote sustainable agriculture and fair trade. By purchasing their produce directly, we ensured that they received fair compensation for their hard work while providing our community with fresh, organic food.",
            "images": "https://example.com/images/story2.jpg",
            "date_created": datetime.utcnow()
        },
        {
            "organization_id": 3,
            "title": "Empowering Women in Tech",
            "content": "We launched a scholarship program to empower women interested in pursuing careers in technology. Through mentorship and financial support, we aim to bridge the gender gap in the tech industry and create more opportunities for talented women.",
            "images": "https://example.com/images/story3.jpg",
            "date_created": datetime.utcnow()
        },
        {
            "organization_id": 4,
            "title": "Providing Clean Water",
            "content": "We installed water purification systems in rural areas to provide clean drinking water to communities in need. Access to clean water is a basic human right, and we are committed to ensuring that everyone has access to this essential resource.",
            "images": "https://example.com/images/story4.jpg",
            "date_created": datetime.utcnow()
        },
        {
            "organization_id": 5,
            "title": "Promoting Renewable Energy",
            "content": "We initiated a solar power project to promote renewable energy and reduce carbon emissions. By harnessing the power of the sun, we are working towards a greener and more sustainable future for our planet.",
            "images": "https://example.com/images/story5.jpg",
            "date_created": datetime.utcnow()
        },
        {
            "organization_id": 6,
            "title": "Rebuilding Communities After Natural Disasters",
            "content": "In the aftermath of a devastating hurricane, we mobilized our resources to rebuild homes and infrastructure in affected communities. Through the collective efforts of volunteers and donors, we provided hope and support to those who were impacted by the disaster.",
            "images": "https://example.com/images/story6.jpg",
            "date_created": datetime.utcnow()
        },
        {
            "organization_id": 7,
            "title": "Empowering Youth Through Education",
            "content": "We established after-school programs and scholarship opportunities to empower underprivileged youth through education. By providing access to quality education and mentorship, we believe in creating a brighter future for the next generation.",
            "images": "https://example.com/images/story7.jpg",
            "date_created": datetime.utcnow()
        },
        {
            "organization_id": 8,
            "title": "Preserving Wildlife and Biodiversity",
            "content": "We worked tirelessly to protect endangered species and preserve biodiversity in fragile ecosystems. Through conservation efforts and community engagement, we strive to maintain the delicate balance of our planet's diverse flora and fauna.",
            "images": "https://example.com/images/story8.jpg",
            "date_created": datetime.utcnow()
        },
        {
            "organization_id": 9,
            "title": "Promoting Mental Health and Well-being",
            "content": "We organized workshops and awareness campaigns to promote mental health and well-being in our community. By breaking the stigma surrounding mental health, we aim to create a supportive environment where individuals can seek help and find solace.",
            "images": "https://example.com/images/story9.jpg",
            "date_created": datetime.utcnow()
        },
        {
            "organization_id": 10,
            "title": "Fighting Hunger and Food Insecurity",
            "content": "Through our food banks and community kitchens, we provided nutritious meals to those facing hunger and food insecurity. Our goal is to ensure that no one goes to bed hungry and that everyone has access to sufficient and healthy food.",
            "images": "https://example.com/images/story10.jpg",
            "date_created": datetime.utcnow()
        }
    ]

    for data in stories_data:
        
        story = Story(**data)
        db.session.add(story)

        db.session.commit()

print("📖 Stories seeded successfully!")

