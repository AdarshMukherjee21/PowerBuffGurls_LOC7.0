from pymongo import MongoClient
from bson.objectid import ObjectId
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

client = MongoClient("mongodb://localhost:27017/")
db = client["csr_project"]

def generate_text_representation(entity):
    if "company_name" in entity:  # Company
        return f"{entity['sector']} {entity['location']} {entity['causes']} {entity['company_size']} {entity['budget']} {' '.join(entity['support_type'])}"
    else:  # NGO
        return f"{entity['locality']} {entity['causes']} {entity['scale']} {entity['funding']} {' '.join(entity['assistance'])} {' '.join(entity['skills'])}"


def match_ngos_for_company(company_name):
    ngos = list(db.ngos.find())
    company = db.companies.find_one({"company_name": company_name})
    if not company:
        return f"Company '{company_name}' not found!"
    
    company_texts = [generate_text_representation(company)]
    ngo_texts = [generate_text_representation(ngo) for ngo in ngos]
    
    vectorizer = TfidfVectorizer()
    all_texts = company_texts + ngo_texts
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    company_vector = tfidf_matrix[0]
    ngo_vectors = tfidf_matrix[1:]
    
    similarity_scores = cosine_similarity(company_vector, ngo_vectors)[0]
    
    matches = sorted(
        [(ngos[i]["ngo_name"], similarity_scores[i]) for i in range(len(ngos))],
        key=lambda x: x[1], reverse=True
    )
    
    return matches

def weighted_match_ngos_for_company(company_name):
    weight_causes = 0.4
    weight_locality = 0.2
    weight_assistance = 0.2
    weight_skills = 0.2
    
    company = db.companies.find_one({"company_name": company_name})
    if not company:
        return f"Company '{company_name}' not found!"
    
    ngos = list(db.ngos.find())
    matches = []
    
    for ngo in ngos:
        score = 0
        
        # Matching causes
        shared_causes = set([company["causes"]]) & set([ngo["causes"]])
        score += weight_causes * (len(shared_causes) / max(len([ngo["causes"]]), 1))
        
        # Matching locality
        if company["location"] == ngo["locality"]:
            score += weight_locality
        
        # Matching assistance
        shared_assistance = set(company["support_type"]) & set(ngo["assistance"])
        score += weight_assistance * (len(shared_assistance) / max(len(ngo["assistance"]), 1))
        
        # Matching skills
        shared_skills = set(company["support_type"]) & set(ngo["skills"])
        score += weight_skills * (len(shared_skills) / max(len(ngo["skills"]), 1))
        
        matches.append((ngo["ngo_name"], score))
    
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches

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