from flask import Flask, jsonify, send_file, request, render_template, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime
from bson import ObjectId
import os

# Initialize Flask app
app = Flask(__name__, static_folder='..', static_url_path='')
CORS(app)

# Initialize MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client.csr_project

# Serve static files
@app.route('/')
def serve_index():
    return send_from_directory('..', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join('..', path)):
        return send_from_directory('..', path)
    return send_from_directory('..', 'index.html')

@app.route('/api/campaigns', methods=['GET'])
def get_campaigns():
    try:
        campaigns = list(db.campaigns.find())
        for campaign in campaigns:
            campaign['_id'] = str(campaign['_id'])
            # Ensure numerical values are properly formatted
            campaign['goal_amount'] = float(campaign.get('goal_amount', 0))
            campaign['amount_raised'] = float(campaign.get('amount_raised', 0))
            
            # Convert date strings to proper format
            if isinstance(campaign.get('start_date'), str):
                campaign['start_date'] = datetime.strptime(campaign['start_date'], '%Y-%m-%d')
            if isinstance(campaign.get('end_date'), str):
                campaign['end_date'] = datetime.strptime(campaign['end_date'], '%Y-%m-%d')
            
        return jsonify(campaigns)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/create_campaign', methods=['POST'])
def create_campaign():
    try:
        campaign_data = request.json
        # Ensure numerical values are properly formatted
        campaign_data['goal_amount'] = float(campaign_data.get('goal_amount', 0))
        campaign_data['amount_raised'] = 0.0
        campaign_data['status'] = 'Active'
        campaign_data['created_at'] = datetime.utcnow()
        
        # Insert campaign
        result = db.campaigns.insert_one(campaign_data)
        
        return jsonify({
            'success': True,
            'campaign_id': str(result.inserted_id)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    try:
        # Get all campaigns
        campaigns = list(db.campaigns.find())
        
        # Calculate totals
        total_campaigns = len(campaigns)
        total_funds_raised = sum(float(c.get('amount_raised', 0)) for c in campaigns)
        lives_impacted = sum(int(c.get('lives_impacted', 0)) for c in campaigns)
        
        return jsonify({
            'total_campaigns': total_campaigns,
            'total_funds_raised': total_funds_raised,
            'lives_impacted': lives_impacted
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)