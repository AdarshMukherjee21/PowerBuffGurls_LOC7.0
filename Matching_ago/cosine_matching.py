from pymongo import MongoClient
from bson.objectid import ObjectId
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["csr_project"]


def generate_text_representation(entity):
    """
    Converts structured data into a text format for vectorization.
    Handles both Companies and NGOs by checking available fields.
    """
    if "sector" in entity:  # This means it's a Company
        return f"{entity['sector']} {entity['locality']} {' '.join(entity['causes_supported'])} {entity['company_size']} {entity['budget']}"
    else:  # This means it's an NGO
        return f"{entity['locality']} {' '.join(entity['causes_supported'])} {entity['operational_scale']} {entity['funding_needs']}"

def match_companies_to_ngos():
    companies = list(db.companies.find())
    ngos = list(db.ngos.find())
    
    # Convert data into text representations
    company_texts = [generate_text_representation(company) for company in companies]
    ngo_texts = [generate_text_representation(ngo) for ngo in ngos]
    
    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer()
    all_texts = company_texts + ngo_texts
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    company_vectors = tfidf_matrix[:len(companies)]
    ngo_vectors = tfidf_matrix[len(companies):]
    
    # Compute Cosine Similarity
    similarity_matrix = cosine_similarity(company_vectors, ngo_vectors)
    
    # Find Best Matches
    matches = []
    for i, company in enumerate(companies):
        best_match_idx = similarity_matrix[i].argmax()
        best_match_score = similarity_matrix[i][best_match_idx]
        best_match_ngo = ngos[best_match_idx]
        
        matches.append({
            "company": company["company_name"],
            "ngo": best_match_ngo["name"],
            "score": best_match_score
        })
    
    return matches

# Execute Matching
matches = match_companies_to_ngos()
print("Matching Results:", matches)
