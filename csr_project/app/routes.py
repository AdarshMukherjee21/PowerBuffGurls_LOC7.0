from flask import Flask, render_template, request, redirect, url_for, session, flash,jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
from app.matching_algorithm import match_ngos_for_company

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super_secret_key_123")
# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["csr_project"]
companies = db["companies"]
ngos = db["ngos"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register/ngo', methods=['GET', 'POST'])
def register_ngo():
    if request.method == 'POST':
        # Retrieve form data
        password = request.form['password']
        ngo_name = request.form['ngo_name']
        contact_name = request.form['contact_name']
        email = request.form['email']
        contact_phone = request.form['contact_phone']
        locality = request.form['locality']
        website = request.form['website']

        # CSR Alignment & Impact
        causes = request.form['causes']
        distance = request.form['distance']
        scale = request.form['scale']
        assistance = request.form.getlist('assistance')  # Multiple selections
        skills = request.form.getlist('skills')  # Multiple selections

        # Financial & Compliance
        funding = request.form['funding']
        transparency = request.form['transparency']
        
        certifications = request.form['certifications']

        # CSR Metrics
        beneficiaries = request.form['beneficiaries']
        sroi = request.form['sroi']
        sdg = request.form['sdg']
        volunteer_hours = request.form['volunteer_hours']
        funds_utilization = request.form['funds_utilization']
        impact_report = request.form['impact_report']
        engagement = request.form['engagement']

        # Check if NGO email already exists
        if ngos.find_one({"email": email}):
            flash("NGO Email already exists! Please login.", "error")
            return redirect(url_for("login_ngo"))

        # Store data in MongoDB
        ngo_data = {
            "password":password,
            "ngo_name": ngo_name,
            "contact_name": contact_name,
            "email": email,
            "contact_phone": contact_phone,
            "locality": locality,
            "website": website,
            "causes": causes,
            "distance": distance,
            "scale": scale,
            "assistance": assistance,
            "skills": skills,
            "funding": funding,
            "transparency": transparency,
            
            "certifications": certifications,
            "beneficiaries": beneficiaries,
            "sroi": sroi,
            "sdg": sdg,
            "volunteer_hours": volunteer_hours,
            "funds_utilization": funds_utilization,
            "impact_report": impact_report,
            "engagement": engagement
        }
        ngos.insert_one(ngo_data)

        flash("NGO registered successfully! Please log in.", "success")
        return redirect(url_for("login_ngo"))

    return render_template('register_ngo.html')

    


@app.route('/register/company', methods=['GET', 'POST'])
def register_company():
    if request.method == 'POST':
        company_name = request.form['company_name']
        sector = request.form['sector']
        contact_name = request.form['contact_name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        location = request.form['location']
        website = request.form['website']
        causes = request.form['causes']
        max_distance = request.form['max_distance']
        ngo_type = request.form['ngo_type']
        support_type = request.form.getlist('support_type')  # Multiple selections
        past_projects = request.form['past_projects']
        budget = request.form['budget']
        tax_bracket = request.form['tax_bracket']
        company_size = request.form['company_size']
        communication_method = request.form['communication_method']
        availability = request.form['availability']

        # Check if company email already exists
        if companies.find_one({"email": email}):
            flash("Company Email already exists! Please login.", "error")
            return redirect(url_for("login_company"))

        # Store data in MongoDB
        company_data = {
            "company_name": company_name,
            "sector": sector,
            "contact_name": contact_name,
            "email": email,
            "password": password,  # No hashing for now
            "phone": phone,
            "location": location,
            "website": website,
            "causes": causes,
            "max_distance": max_distance,
            "ngo_type": ngo_type,
            "support_type": support_type,
            "past_projects": past_projects,
            "budget": budget,
            "tax_bracket": tax_bracket,
            "company_size": company_size,
            "communication_method": communication_method,
            "availability": availability
        }
        companies.insert_one(company_data)

        flash("Company registered successfully! Please log in.", "success")
        return redirect(url_for("login_company"))

    return render_template('register_company.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/ngo', methods=['GET', 'POST'])
def login_ngo():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        ngo = ngos.find_one({"email": email})  # Fetch NGO data

        if ngo:
            if ngo["password"] == password:  # Check if password matches
                session["ngo_email"] = email
                flash("NGO Login successful!", "success")
                return redirect(url_for("dashboard_ngo"))  # Redirect to NGO dashboard
            
            else:
                flash("Incorrect password. Try again!", "error")
                return redirect(url_for("login_ngo"))  # Reload login page
        
        else:
            flash("Email not found. Please register!", "error")
            return redirect(url_for("register_ngo"))  # Ask user to register

    return render_template('login_ngo.html')


@app.route('/login/company', methods=['GET', 'POST'])
def login_company():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        company = companies.find_one({"email": email})  # Fetch company data

        if company:
            if company["password"] == password:  # Check if password matches
                session["company_email"] = email
                flash("Company Login successful!", "success")
                return redirect(url_for("dashboard_company"))  # Redirect to dashboard
            
            else:
                flash("Incorrect password. Try again!", "error")
                return redirect(url_for("login_company"))  # Reload login page
        
        else:
            flash("Email not found. Please register!", "error")
            return redirect(url_for("register_company"))  # Ask user to register

    return render_template('login_company.html')


@app.route('/dashboard/ngo')
def dashboard_ngo():
    if "ngo_email" not in session:
        flash("Please log in first!", "error")
        return redirect(url_for("login_ngo"))

    ngo_email = session["ngo_email"]
    ngo = ngos.find_one({"email": ngo_email})

    if not ngo:
        flash("NGO profile not found!", "error")
        return redirect(url_for("login_ngo"))

    # Get the current date
    today = datetime.today().strftime('%Y-%m-%d')

    upcoming_events = []
    hosted_events = []

    # Ensure the NGO has an events field
    if "events" in ngo:
        for event in ngo["events"]:
            if event["event_date"] >= today:
                upcoming_events.append(event)
            else:
                hosted_events.append(event)
                
                # Move hosted events to past_collab if not already present
                ngos.update_one(
                    {"email": ngo_email},
                    {"$set": {f"past_collab.{event['event_name']}": []}}  # Empty list for now
                )

    return render_template(
        "dashboard_ngo.html",
        ngo=ngo,
        upcoming_events=upcoming_events,
        hosted_events=hosted_events
    )

@app.route('/upload_event', methods=['GET', 'POST'])
def upload_event():
    if "ngo_email" not in session:
        flash("Please log in first!", "error")
        return redirect(url_for("login_ngo"))

    if request.method == "POST":
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        budget = request.form['budget']
        volunteers_required = request.form['volunteers_required']
        ngo_host = session["ngo_email"]  # Get logged-in NGO email

        # Find NGO in database
        ngo = ngos.find_one({"email": ngo_host})

        if ngo:
            # Create the event object
            event_data = {
                "event_name": event_name,
                "event_date": event_date,
                "budget": budget,
                "volunteers_required": volunteers_required,
                "ngo_host": ngo_host
            }
            
            # Append event to the NGO's events list
            ngos.update_one(
                {"email": ngo_host},
                {"$push": {"events": event_data}}
            )

            flash("Event uploaded successfully!", "success")
            return redirect(url_for("dashboard_ngo"))

    return render_template("upload_event.html")

@app.route('/search_companies')
def search_companies():
    # TODO: Implement company search functionality
    return "Search for Companies page (To be implemented)"



@app.route('/dashboard/company')
def dashboard_company():
    if "company_email" not in session:
        flash("Please log in first!", "error")
        return redirect(url_for("login_company"))

    company_email = session["company_email"]

    # Fetch company details
    company = companies.find_one({"email": company_email})

    if not company:
        flash("Company not found!", "error")
        return redirect(url_for("login_company"))

    # Fetch followed NGOs
    followed_ngos = company.get("followed_ngos", [])  # Get followed NGOs, default to empty list

    # Get upcoming events from followed NGOs
    followed_ngos_events = []
    for ngo_email in followed_ngos:
        ngo = ngos.find_one({"email": ngo_email})
        if ngo and "events" in ngo:
            for event in ngo["events"]:
                if event["event_date"] >= datetime.now().strftime("%Y-%m-%d"):  # Check if event is upcoming
                    followed_ngos_events.append(event)

    # Get events company is partaking in
    participating_events = company.get("participating_events", [])

    return render_template("dashboard_company.html",
                           company=company,
                           followed_ngos_events=followed_ngos_events,
                           participating_events=participating_events)


@app.route('/search_ngos', methods=['GET', 'POST'])
def search_ngos():
    # Functionality to search for NGOs will be implemented here
    return render_template("search_ngos.html")





@app.route('/match_event', methods=['GET'])
def match_event():
    # Functionality to match with an event will be implemented here
    return render_template("match_event.html")


from app.matching_algorithm import match_ngos_for_company, match_companies_for_ngo


@app.route('/match_ngo')
def match_ngo():
    if "company_email" not in session:
        return "Please log in first!", 403

    company = db.companies.find_one({"email": session["company_email"]})
    if not company:
        return "Company not found!", 404

    matches = match_ngos_for_company(company["company_name"])  # Call matching algorithm
    session["ngo_matches"] = matches
    session["current_ngo_index"] = 0

    return render_template("match_ngo.html")

@app.route('/match_company')
def match_company():
    if "ngo_email" not in session:
        return "Please log in first!", 403

    ngo = db.ngos.find_one({"email": session["ngo_email"]})
    if not ngo:
        return "NGO not found!", 404

    matches = match_companies_for_ngo(ngo["ngo_name"])  # Call matching algorithm
    session["company_matches"] = matches
    session["current_company_index"] = 0

    return render_template("match_company.html")

@app.route('/next_ngo')
def next_ngo():
    if "ngo_matches" not in session or session["current_ngo_index"] >= len(session["ngo_matches"]):
        return jsonify({"status": "done"})  # No more matches

    ngo_name, score = session["ngo_matches"][session["current_ngo_index"]]
    session["current_ngo_index"] += 1

    ngo_details = db.ngos.find_one({"ngo_name": ngo_name}, {"_id": 0})
    return jsonify({"ngo": ngo_details, "score": score})

@app.route('/next_company')
def next_company():
    if "company_matches" not in session or session["current_company_index"] >= len(session["company_matches"]):
        return jsonify({"status": "done"})  # No more matches

    company_name, score = session["company_matches"][session["current_company_index"]]
    session["current_company_index"] += 1

    company_details = db.companies.find_one({"company_name": company_name}, {"_id": 0})
    return jsonify({"company": company_details, "score": score})

@app.route('/like_ngo', methods=['POST'])
def like_ngo():
    if "company_email" not in session:
        return "Unauthorized", 403

    data = request.json
    ngo_name = data.get("ngo_name")

    db.companies.update_one(
        {"email": session["company_email"]},
        {"$addToSet": {"followed_ngos": ngo_name}}  # Save liked NGO
    )

    return jsonify({"status": "liked"})

@app.route('/like_company', methods=['POST'])
def like_company():
    if "ngo_email" not in session:
        return "Unauthorized", 403

    data = request.json
    company_name = data.get("company_name")

    db.ngos.update_one(
        {"email": session["ngo_email"]},
        {"$addToSet": {"followed_companies": company_name}}  # Save liked company
    )

    return jsonify({"status": "liked"})




@app.route('/logout')
def logout():
    session.pop("company_email", None)
    session.pop("ngo_email", None)
    flash("Logged out successfully!", "success")
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)
