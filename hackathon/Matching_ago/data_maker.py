from pymongo import MongoClient
from bson.objectid import ObjectId
import random

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["csr_project"]

def generate_dummy_data():
    ngos = []
    companies = []
    causes_list = ["Education", "Healthcare", "Environment", "Poverty Alleviation", "Animal Welfare"]
    assistance_types = ["Financial Aid", "Volunteering", "Training", "Logistics Support"]
    skills_needed = ["Marketing", "Fundraising", "Legal Aid", "IT Support"]
    support_types = ["Funding", "Manpower", "Technical Support", "CSR Partnerships"]
    communication_methods = ["Email", "Phone", "In-Person Meetings"]
    
    for i in range(30):
        ngos.append({
            "password": "password123",
            "ngo_name": f"NGO_{i}",
            "contact_name": f"Contact_{i}",
            "email": f"ngo{i}@example.com",
            "contact_phone": f"+9112345678{i%10}",
            "locality": f"City_{i%5}",
            "website": f"http://ngo{i}.org",
            "causes": random.choice(causes_list),
            "distance": random.randint(5, 50),
            "scale": random.choice(["Local", "National", "International"]),
            "assistance": random.sample(assistance_types, random.randint(1, 3)),
            "skills": random.sample(skills_needed, random.randint(1, 3)),
            "funding": random.randint(10000, 500000),

            "certifications": f"Cert_{i%3}",
            "beneficiaries": random.randint(100, 10000),
            "sroi": round(random.uniform(1.0, 5.0), 2),
            "sdg": f"SDG_{random.randint(1, 17)}",
            "volunteer_hours": random.randint(100, 5000),
            "impact_report": f"Report_{i}.pdf",
            "engagement": random.choice(["High", "Medium", "Low"])
        })
    
    for i in range(20):
        companies.append({
            "company_name": f"Company_{i}",
            "sector": random.choice(["Tech", "Finance", "Healthcare", "Retail", "Manufacturing"]),
            "contact_name": f"Contact_{i}",
            "email": f"company{i}@example.com",
            "password": "password123",
            "phone": f"+9198765432{i%10}",
            "location": f"City_{i%5}",
            "website": f"http://company{i}.com",
            "causes": random.choice(causes_list),
            "max_distance": random.randint(10, 100),
            "ngo_type": random.choice(["Education", "Healthcare", "Environment"]),
            "support_type": random.sample(support_types, random.randint(1, 3)),
            "past_projects": [f"NGO_{random.randint(0, 29)}" for _ in range(random.randint(0, 5))],
            "budget": random.randint(50000, 2000000),
            "tax_bracket": random.choice(["10%", "20%", "30%"]),
            "company_size": random.choice(["Small", "Medium", "Large"]),
            "communication_method": random.choice(communication_methods),
            "availability": random.choice(["Weekdays", "Weekends", "Flexible"])
        })
    
    db.ngos.insert_many(ngos)
    db.companies.insert_many(companies)
    print("Dummy data inserted successfully!")

generate_dummy_data()
