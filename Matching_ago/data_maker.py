from pymongo import MongoClient
# from bson.objectid import ObjectId
import random

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["csr_project"]

# Company Schema
def create_company(company_name, sector, locality, budget, tax_bracket, causes_supported, company_size, max_distance, rating, website):
    return {
        "company_name": company_name,
        "sector": sector,
        "locality": locality,
        "budget": budget,
        "tax_bracket": tax_bracket,
        "causes_supported": causes_supported,
        "company_size": company_size,
        "max_distance": max_distance,
        "rating": rating,
        "website": website
    }

# NGO Schema
def create_ngo(name, locality, causes_supported, funding_needs, operational_scale, volunteer_skills, max_distance, rating, certifications, website):
    return {
        "name": name,
        "locality": locality,
        "causes_supported": causes_supported,
        "funding_needs": funding_needs,
        "operational_scale": operational_scale,
        "volunteer_skills": volunteer_skills,
        "max_distance": max_distance,
        "rating": rating,
        "certifications": certifications,
        "website": website
    }

# Dummy Data Generation
sectors = ["Technology", "Finance", "Healthcare", "Retail", "Manufacturing", "Energy"]
causes = ["Education", "Healthcare", "Environment", "Poverty", "Animal Welfare", "Women Empowerment"]
localities = ["New York", "San Francisco", "London", "Berlin", "Mumbai", "Tokyo"]
tax_brackets = ["5%", "10%", "15%", "20%", "25%"]
company_sizes = ["Small", "Medium", "Large"]
ratings = [3.5, 4.0, 4.5, 5.0]
operational_scales = ["Local", "National", "International"]
skills = ["IT", "Medical", "Management", "Education", "Engineering"]
certifications = ["80G", "FCRA", "ISO 9001", "NGO DARPAN"]

# Generate 20 Companies
companies = [
    create_company(f"Company_{i}", random.choice(sectors), random.choice(localities), 
                   random.randint(10000, 500000), random.choice(tax_brackets), 
                   random.sample(causes, 2), random.choice(company_sizes),
                   random.randint(10, 100), random.choice(ratings), f"www.company{i}.com")
    for i in range(20)
]

db.companies.insert_many(companies)

# Generate 30 NGOs
ngos = [
    create_ngo(f"NGO_{i}", random.choice(localities), random.sample(causes, 2),
               random.randint(5000, 200000), random.choice(operational_scales),
               random.sample(skills, 2), random.randint(10, 100),
               random.choice(ratings), random.sample(certifications, 2),
               f"www.ngo{i}.org")
    for i in range(30)
]

db.ngos.insert_many(ngos)

print("Inserted 20 companies and 30 NGOs successfully!")
