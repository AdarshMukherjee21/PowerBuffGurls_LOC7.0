from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Update if needed

# Select Database
db = client["csr_database"]

# Collections
companies_collection = db["companies"]
ngos_collection = db["ngos"]
users_collection = db["users"]  # If you're handling authentication separately
