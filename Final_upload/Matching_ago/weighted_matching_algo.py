from pymongo import MongoClient
# from bson.objectid import ObjectId
import random

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["csr_project"]

# Weighted Matching Algorithm
def calculate_match_score(company, ngo):
    score = 0
    weights = {
        "causes_supported": 5,
        "locality": 3,
        "max_distance": 2,
        "budget": 4,
        "rating": 1
    }
    
    if set(company["causes_supported"]) & set(ngo["causes_supported"]):
        score += weights["causes_supported"]
    if company["locality"] == ngo["locality"]:
        score += weights["locality"]
    if company["max_distance"] >= ngo["max_distance"]:
        score += weights["max_distance"]
    if company["budget"] >= ngo["funding_needs"]:
        score += weights["budget"]
    score += ((company["rating"] + ngo["rating"]) / 2) * weights["rating"]
    
    return score

# Match Companies to NGOs
def match_companies_to_ngos():
    matched_pairs = []
    companies = list(db.companies.find())
    ngos = list(db.ngos.find())
    
    for company in companies:
        best_match = None
        best_score = -1
        
        for ngo in ngos:
            score = calculate_match_score(company, ngo)
            if score > best_score:
                best_match = ngo
                best_score = score
        
        if best_match:
            matched_pairs.append({
                "company": company["company_name"],
                "ngo": best_match["name"],
                "score": best_score
            })
    
    return matched_pairs

# Execute Matching
matches = match_companies_to_ngos()
print("Matching Results:", matches)