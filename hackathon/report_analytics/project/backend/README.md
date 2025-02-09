# CSR Portal Backend

This is the backend service for the CSR Portal, built with Flask and MongoDB.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure MongoDB is running locally on port 27017

3. Start the server:
```bash
python main.py
```

## API Endpoints

- GET `/companies` - List all companies
- GET `/ngos` - List all NGOs
- GET `/companies/{company_name}` - Get company details
- GET `/ngos/{ngo_name}` - Get NGO details
- POST `/companies/login` - Company login
- POST `/ngos/login` - NGO login
- GET `/match/{company_name}` - Get matching NGOs for a company
- GET `/impact/{ngo_name}` - Get impact metrics for an NGO