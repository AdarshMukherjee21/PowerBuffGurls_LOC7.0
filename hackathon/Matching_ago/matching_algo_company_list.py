from pymongo import MongoClient
from bson.objectid import ObjectId
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["csr_project"]

def generate_text_representation(entity):
    if "company_name" in entity:  # Company
        return f"{entity['sector']} {entity['location']} {entity['causes']} {entity['company_size']} {entity['budget']}"
    else:  # NGO
        return f"{entity['locality']} {entity['causes']} {entity['scale']} {entity['funding']}"

def match_companies_for_ngo(ngo_name):
    companies = list(db.companies.find())
    ngo = db.ngos.find_one({"ngo_name": ngo_name})
    if not ngo:
        return f"NGO '{ngo_name}' not found!"
    
    ngo_texts = [generate_text_representation(ngo)]
    company_texts = [generate_text_representation(company) for company in companies]
    
    vectorizer = TfidfVectorizer()
    all_texts = ngo_texts + company_texts
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    ngo_vector = tfidf_matrix[0]
    company_vectors = tfidf_matrix[1:]
    
    similarity_scores = cosine_similarity(ngo_vector, company_vectors)[0]
    
    matches = sorted(
        [(companies[i]["company_name"], similarity_scores[i]) for i in range(len(companies))],
        key=lambda x: x[1], reverse=True
    )
    
    return matches

def weighted_match_companies_for_ngo(ngo_name):
    weight_causes = 0.5
    weight_locality = 0.3
    weight_rating = 0.2
    
    ngo = db.ngos.find_one({"ngo_name": ngo_name})
    if not ngo:
        return f"NGO '{ngo_name}' not found!"
    
    companies = list(db.companies.find())
    matches = []
    
    for company in companies:
        score = 0
        shared_causes = set([company["causes"]]) & set([ngo["causes"]])
        score += weight_causes * (len(shared_causes) / max(len([ngo["causes"]]), 1))
        if company["location"] == ngo["locality"]:
            score += weight_locality
        score += weight_rating * (company.get("rating", 0) / 5.0)
        matches.append((company["company_name"], score))
    
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches

# Example Usage
ngo_name_input = "NGO_1"
print("\nCosine Similarity Matches:")
print(match_companies_for_ngo(ngo_name_input))

print("\nWeighted Matching Results:")
print(weighted_match_companies_for_ngo(ngo_name_input))