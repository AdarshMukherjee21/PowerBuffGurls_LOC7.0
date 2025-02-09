from pymongo import MongoClient
import google.generativeai as genai
from typing import Dict
import sys

# Configure Gemini API
try:
    genai.configure(api_key="AIzaSyCC6GPbq45ttTt28jkdR-FSvtxTyx6HpEU ")
    # Initialize the model
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    sys.exit(1)

# Connect to MongoDB with error handling
try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    # Test the connection
    client.server_info()
    db = client["csr_project"]
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    sys.exit(1)

def calculate_csr_fit(company: Dict, ngo: Dict) -> float:

    print("_____________________________CSR__METRIC________________________________________________")
    """
    Calculate CSR Fit Score between a company and NGO.
    
    Args:
        company (Dict): Company information
        ngo (Dict): NGO information
        
    Returns:
        float: CSR fit score between 0 and 100
    """
    score = 0

    # Cause Alignment (40%)
    if company.get("causes") == ngo.get("causes"):
        score += 40

    # Distance Factor (10%)
    max_distance = company.get("max_distance", 0)
    if max_distance > 0 and ngo.get("distance", float('inf')) <= max_distance:
        score += 10 * (1 - (ngo.get("distance", 0) / max_distance))

    # Past Collaborations (10%)
    if company.get("company_name") in ngo.get("past_collab", []):
        score += 10

    # Funding & Budget Match (15%)
    company_budget = company.get("budget", 0)
    if company_budget > 0:
        budget_match = min(ngo.get("funding", 0) / company_budget, 1)
        score += budget_match * 15

    # SROI (15%)
    score += min(ngo.get("sroi", 0) / 10, 1) * 15

    # Engagement Level (10%)
    engagement_scores = {"High": 10, "Medium": 5, "Low": 2}
    score += engagement_scores.get(ngo.get("engagement", "Low"), 0)

    return round(score, 2)

def get_partnership_insights(company: Dict, ngo: Dict, score: float) -> str:
    print("________________________________PATRNER_SHITP_INSIGHTS_______________________________________________")
    """
    Get AI-generated partnership insights using Gemini.
    
    Args:
        company (Dict): Company information
        ngo (Dict): NGO information
        score (float): CSR fit score
        
    Returns:
        str: Generated insights
    """
    prompt = f"""A company named {company.get('company_name')} (sector: {company.get('sector', 'Unknown')}) 
    is considering partnering with {ngo.get('ngo_name')} (focus: {ngo.get('causes', 'Unknown')}). 
    Their CSR Fit Score is {score}/100. Provide insights on:
    1. How this partnership can benefit both parties.
    2. Potential PR and branding benefits.
    3. Key challenges they might face.
    Keep the response under 100 words.
    
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating insights: {e}"

def main(company_name: str, ngo_name: str):
    # Fetch example company and NGO from MongoDB with error handling
    company = db.companies.find_one({"company_name": company_name})
    ngo = db.ngos.find_one({"ngo_name": ngo_name})

    if not company or not ngo:
        print("Company or NGO not found in the database.")
        return

    try:
        # Compute CSR Fit Score
        csr_fit_score = calculate_csr_fit(company, ngo)
        print(f"CSR Fit Score for {company.get('company_name')} and {ngo.get('ngo_name')}: {csr_fit_score}/100")
        
        # Get AI-generated insights
        insights = get_partnership_insights(company, ngo, csr_fit_score)
        print("\nPartnership Insights:")
        print(insights)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    # You can call the function with desired company and NGO names
    main("Company_19", "NGO_1")
