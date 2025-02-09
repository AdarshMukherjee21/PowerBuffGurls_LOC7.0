from flask import Flask, render_template, request, redirect, url_for, session, flash,jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
from app.matching_algorithm_OG import match_ngos_for_company
from urllib.parse import unquote

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super_secret_key_123")
# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["csr_project"]
companies = db["companies"]
ngos = db["ngos"]
friend_requests = db["friend_requests"]

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
    print(f"Logged-in NGO Email: {ngo_email}")  # Debug: Check ngo_email from session

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

    # Fetch friend requests for the logged-in NGO
    friend_requests = db['friend_requests'].find({"ngo_name": ngo["ngo_name"], "status": "Pending"})
    friend_requests_list = list(friend_requests)  # Convert cursor to list for rendering

    print(f"Friend Requests List: {friend_requests_list}")  # Debug: Check the friend requests list

    # Fetch friends list from the NGO document (optional)
    friends = ngo.get("friends", [])  # You can fetch the friends list from the NGO document

    return render_template(
        "dashboard_ngo.html",
        ngo=ngo,
        upcoming_events=upcoming_events,
        hosted_events=hosted_events,
        friend_requests=friend_requests_list,  # Pass friend requests to the template
        friends=friends  # Pass friends list to the template
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

@app.route('/search_companies', methods=['GET', 'POST'])
def search_companies():
    companies = []

    if request.method == "POST":
        search_query = request.form.get("search_query", "").strip()
        if search_query:
            companies = list(db.companies.find({"company_name": {"$regex": search_query, "$options": "i"}}))

    return render_template("search_companies.html", companies=companies)




@app.route('/dashboard/company')
def dashboard_company():
    if "company_email" not in session:
        flash("Please log in first!", "error")
        return redirect(url_for("login_company"))

    company_email = session["company_email"]

    # Debugging: Check if the company_email is correctly retrieved from session
    print(f"[DEBUG] Logged in company email: {company_email}")

    # Fetch company details using email
    company = companies.find_one({"email": company_email})

    # Debugging: Check if the company data is fetched correctly
    print(f"[DEBUG] Company data: {company}")

    if not company:
        flash("Company not found!", "error")
        return redirect(url_for("login_company"))

    # Fetch pending friend requests using the company name
    company_name = company["company_name"]
    friend_requests = db['friend_requests'].find({
        "company_name": company_name,  # Querying by company_name
        "status": "Pending"
    })

    # Debugging: Check if the pending friend requests are fetched correctly
    friend_requests_list = list(friend_requests)
    print(f"[DEBUG] Pending Friend Requests for company '{company_name}': {friend_requests_list}")

    if not friend_requests_list:
        print("[DEBUG] No pending friend requests.")
        flash("No pending friend requests.", "info")

    # Fetch accepted friend requests (NGOs that the company is friends with)
    accepted_friends = db.friend_requests.find({"company_email": company_email, "status": "Accepted"})

    # Debugging: Check if accepted friends (NGOs) are fetched correctly
    accepted_friends_list = list(accepted_friends)
    print(f"[DEBUG] Accepted friends: {accepted_friends_list}")

    # Get NGO emails from accepted friends
    ngo_emails = []
    for friend in accepted_friends_list:
        ngo_name = friend["ngo_name"]
        ngo = ngos.find_one({"ngo_name": ngo_name})

        # Debugging: Check if NGO email is fetched correctly
        if ngo:
            ngo_email = ngo["email"]
            ngo_emails.append(ngo_email)
            print(f"[DEBUG] NGO email for {ngo_name}: {ngo_email}")
        else:
            print(f"[DEBUG] NGO with name {ngo_name} not found")

    # Get upcoming events from accepted NGOs
    followed_ngos_events = []
    for ngo_email in ngo_emails:
        ngo = ngos.find_one({"email": ngo_email})

        # Debugging: Check if NGO data is fetched correctly
        if ngo:
            print(f"[DEBUG] Fetched NGO: {ngo}")
            if "events" in ngo:
                for event in ngo["events"]:
                    if event["event_date"] >= datetime.now().strftime("%Y-%m-%d"):  # Check if event is upcoming
                        followed_ngos_events.append(event)
                        print(f"[DEBUG] Upcoming event found: {event['event_name']} hosted by {ngo_email}")
            else:
                print(f"[DEBUG] No events found for NGO {ngo_email}")
        else:
            print(f"[DEBUG] NGO with email {ngo_email} not found")

    # Check the events for the company (participating events)
    participating_events = []
    for event in followed_ngos_events:
        # Check if company is participating in the event
        if company_email in event.get("participants", []):
            participating_events.append(event)
            print(f"[DEBUG] Company {company_email} is participating in event: {event['event_name']}")
        else:
            print(f"[DEBUG] Company {company_email} is NOT participating in event: {event['event_name']}")

    # Debugging: Check the final list of followed NGOs' events and participating events
    print(f"[DEBUG] Followed NGOs Events: {followed_ngos_events}")
    print(f"[DEBUG] Participating Events: {participating_events}")

    # Passing the data to the template
    return render_template("dashboard_company.html",
                           company=company,
                           followed_ngos_events=followed_ngos_events,
                           participating_events=participating_events,
                           friend_requests=friend_requests_list)


@app.route('/search_ngos', methods=['GET', 'POST'])
def search_ngos():
    ngos = []
    
    if request.method == "POST":
        search_query = request.form.get("search_query", "").strip()
        if search_query:
            ngos = list(db.ngos.find({"ngo_name": {"$regex": search_query, "$options": "i"}}))

    return render_template("search_ngos.html", ngos=ngos)








from app.matching_algorithm_OG import match_ngos_for_company, match_companies_for_ngo


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

@app.route('/match_event/<event_name>', methods=['GET', 'POST'])
def match_event(event_name):
    if "company_email" not in session:
        flash("Please log in first!", "error")
        return redirect(url_for("login_company"))

    company_email = session["company_email"]
    
    # Fetch company details
    company = companies.find_one({"email": company_email})
    
    if not company:
        flash("Company not found!", "error")
        return redirect(url_for("login_company"))

    # Fetch the event details by event_name
    event = None
    for ngo in ngos.find():  # Assuming NGOs are stored in the 'ngos' collection
        for e in ngo.get("events", []):
            if e["event_name"] == event_name:
                event = e
                ngo_email = ngo["email"]
                break
    
    if not event:
        flash("Event not found!", "error")
        return redirect(url_for("dashboard_company"))
    
    # Handle POST request to add company as a collaborator
    if request.method == "POST":
        # Update the event with the company as a collaborator
        updated = ngos.update_one(
            {"email": ngo_email, "events.event_name": event_name},
            {"$addToSet": {"events.$.collaborators": company["company_name"]}}
        )

        if updated.modified_count > 0:
            flash(f"{company['company_name']} has been added as a collaborator to the event!", "success")
        else:
            flash("Failed to add collaborator.", "error")

        return redirect(url_for('dashboard_company'))  # Redirect back to company dashboard
    
    return render_template("match_event.html", event=event)


@app.route('/next_ngo')
def next_ngo():
    # Debugging session values
    print("NGO Matches:", session.get("ngo_matches"))
    print("Current NGO Index:", session.get("current_ngo_index"))

    # Check if ngo_matches or current_ngo_index are missing or if there are no more matches
    if "ngo_matches" not in session or session["current_ngo_index"] >= len(session["ngo_matches"]):
        print("No more matches available or ngo_matches is empty")
        return jsonify({"status": "done"})  # No more matches

    ngo_name, score = session["ngo_matches"][session["current_ngo_index"]]
    session["current_ngo_index"] += 1

    # Debugging the NGO name and score
    print("Fetching NGO:", ngo_name, "with score:", score)

    # Fetch NGO details from the database using ngo_name
    ngo_details = db.ngos.find_one({"ngo_name": ngo_name}, {"_id": 0})
    
    # Debugging the NGO details fetched from DB
    if not ngo_details:
        print(f"NGO {ngo_name} not found in database.")
    else:
        print(f"Fetched NGO details: {ngo_details}")

    return jsonify({"ngo": ngo_details, "score": score})



@app.route('/next_company')
def next_company():
    if "company_matches" not in session or session["current_company_index"] >= len(session["company_matches"]):
        return jsonify({"status": "done"})  # No more matches

    company_name, score = session["company_matches"][session["current_company_index"]]
    session["current_company_index"] += 1

    company_details = db.companies.find_one({"company_name": company_name}, {"_id": 0})
    return jsonify({"company": company_details, "score": score})



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

    return render_template("match_company.html")  # Render the same template for NGOs



@app.route('/like_ngo', methods=['POST'])
def like_ngo():
    try:
        # Ensure company is logged in by checking the session
        company_email = session.get("company_email")
        
        if not company_email:
            return jsonify({"error": "Unauthorized"}), 403  # If company isn't logged in, return an error

        # Get JSON data from the request
        data = request.get_json()
        ngo_email = data.get("ngo_email")

        # Validate NGO email
        if not ngo_email:
            return jsonify({"error": "NGO email is required"}), 400

        # Retrieve the company document using the company email
        company = db.companies.find_one({"email": company_email})
        if not company:
            return jsonify({"error": "Company not found"}), 404
        
        # Get the company name from the retrieved company document
        company_name = company.get("company_name")
        
        if not company_name:
            return jsonify({"error": "Company name not found"}), 404
        
        # Retrieve the NGO document using the NGO email
        ngo = db.ngos.find_one({"email": ngo_email})
        if not ngo:
            return jsonify({"error": "NGO not found"}), 404
        
        # Add the NGO to the company's followed NGOs
        db.companies.update_one(
            {"email": company_email},
            {"$addToSet": {"followed_ngos": ngo_email}}  # Add the NGO's email to the followed list
        )

        # Optionally, add a friend request between the company and the NGO
        friend_request_data = {
            "company_name": company_name,
            "ngo_email": ngo_email,
            "status": "pending"
        }
        db.friend_requests.insert_one(friend_request_data)

        return jsonify({"status": "liked", "message": "Follow request sent to NGO"}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "An error occurred"}), 500


@app.route('/like_company', methods=['POST'])
def like_company():
    try:
        data = request.get_json()  # Get JSON data from the request

        # Debugging: Log incoming data
        print(f"Received data: {data}")

        company_name = data.get("company_name")
        ngo_email = data.get("ngo_email")

        # Retrieve the company and NGO information from the database
        liking_company = db.companies.find_one({"company_name": company_name})
        ngo = db.ngos.find_one({"email": ngo_email})

        # Debugging: Check if the company and NGO are found
        if liking_company:
            print(f"Found company: {liking_company}")
            company_email = liking_company.get("email")  # Get the company's email
        else:
            print("Company not found")
            company_email = None

        if ngo:
            print(f"Found NGO: {ngo}")
            ngo_name = ngo.get("ngo_name")  # Get the NGO's name
        else:
            print("NGO not found")
            ngo_name = None

        # Check if both company and NGO are found
        if liking_company and ngo:
            request_data = {
                "company_name": company_name,
                  # Include the company's email
                # Include the NGO's name
                "ngo_email": ngo_email,  # Include the NGO's email
                "status": "pending"  # Status of the request
            }

            print(f"Inserting request: {request_data}")
            db.friend_requests.insert_one(request_data)

            print("Follow request sent successfully.")
            return jsonify({"message": "Follow request sent successfully."}), 200
        else:
            print("Error: Company or NGO not found.")
            return jsonify({"error": "Company or NGO not found."}), 404
    except Exception as e:
        print(f"Exception: {str(e)}")
        return jsonify({"error": str(e)}), 500


# from flask import render_template, request, redirect, url_for, session
from bson.objectid import ObjectId
# from app import app, db

@app.route('/event/<event_name>', methods=['GET'])
def view_event(event_name):
    if "ngo_email" not in session:
        return redirect(url_for("login_ngo"))

    # Find the NGO document containing the event
    ngo = db.ngos.find_one({"events.event_name": event_name})

    if not ngo:
        return "Event not found!", 404

    # Extract the event from the list of events
    event = next((e for e in ngo["events"] if e["event_name"] == event_name), None)

    if not event:
        return "Event not found!", 404

    # Check if the event has the 'collaborators' field; if not, set it as an empty list
    if "collaborators" not in event:
        event["collaborators"] = []

    # Get the collaborators (can be an empty list if no collaborators are set)
    collaborators = event["collaborators"]

    return render_template("event_details.html", event=event, collaborators=collaborators)

@app.route('/event/<event_name>/add_collaborators', methods=['GET', 'POST'])
def add_collaborators(event_name):
    if "ngo_email" not in session:
        return redirect(url_for("login_ngo"))

    # Find the NGO document containing the event
    ngo = db.ngos.find_one({"events.event_name": event_name})

    if not ngo:
        return "Event not found!", 404

    # Extract the event from the list of events
    event = next((e for e in ngo["events"] if e["event_name"] == event_name), None)

    if not event:
        return "Event not found!", 404

    # Ensure the 'collaborators' field exists in the event
    if "collaborators" not in event:
        event["collaborators"] = []

    # Get list of existing friends
    friends = ngo.get("friends", [])
    
    # Get the companies in the system
    companies = db.companies.find({})  # Adjust this query as per your schema

    if request.method == "POST":
        # Handle adding collaborators (friends or companies)
        selected_collaborators = request.form.getlist("collaborators")  # List of selected collaborators

        # Update the event's collaborators in the database
        db.ngos.update_one(
            {"_id": ngo["_id"], "events.event_name": event_name},
            {"$addToSet": {"events.$.collaborators": {"$each": selected_collaborators}}}
        )
        
        return redirect(url_for('view_event', event_name=event_name))

    return render_template("add_collaborators.html", event=event, friends=friends, companies=companies)


@app.route('/event/<event_name>/update', methods=['GET', 'POST'])
def update_event(event_name):
    if "ngo_email" not in session:
        return redirect(url_for("login_ngo"))

    # Find the NGO document that contains the event
    ngo = db.ngos.find_one({"events.event_name": event_name})

    if not ngo:
        return "Event not found!", 404

    # Extract the event from the list of events
    event = next((e for e in ngo["events"] if e["event_name"] == event_name), None)

    if not event:
        return "Event not found!", 404

    # Handle form submission to update event details
    if request.method == "POST":
        updated_data = {
            "event_description": request.form["event_description"],
            "budget": request.form["budget"],
            "volunteers_required": request.form["volunteers_required"]
        }

        # Update the event in the NGO's events list
        db.ngos.update_one(
            {"_id": ngo["_id"], "events.event_name": event_name},
            {"$set": {
                "events.$.event_description": updated_data["event_description"],
                "events.$.budget": updated_data["budget"],
                "events.$.volunteers_required": updated_data["volunteers_required"]
            }}
        )
        
        # Redirect back to the event details page after updating
        return redirect(url_for('view_event', event_name=event_name))

    return render_template("update_event.html", event=event)


@app.route('/ngo_friends')
def ngo_friends():
    if 'ngo_id' not in session:
        flash("You must be logged in as an NGO.", "error")
        return redirect(url_for('login'))

    ngo_id = session['ngo_id']
    ngo = db.ngos.find_one({'_id': ObjectId(ngo_id)})

    return render_template('ngo_friends.html', friends=ngo.get('friends', []))

@app.route('/send_friend_request/<ngo_name>', methods=['POST'])
def send_friend_request(ngo_name):
    # Retrieve company email from session
    company_email = session.get('company_email')
    
    if not company_email:
        flash('You need to be logged in as a company to send a friend request.', 'error')
        return redirect(url_for('login_company'))

    # Debug: Check if the company email is in the session
    print(f"[DEBUG] Company Email from session: {company_email}")

    # Retrieve company details using the email
    company = companies.find_one({"email": company_email})
    
    if not company:
        flash('Company not found!', 'error')
        return redirect(url_for('login_company'))
    
    # Create friend request data
    request_data = {
        "company_email": company_email,
        "ngo_name": ngo_name,
        "status": "Pending"
    }

    # Assuming you have a collection to store friend requests
    friend_requests.insert_one(request_data)

    flash(f'Friend request sent to {ngo_name}!', 'success')
    return redirect(url_for('search_ngos'))  # Redirect back to search page or wherever you want

@app.route('/send_friend_request_company/<company_name>', methods=['POST'])
def send_friend_request_company(company_name):
    # Retrieve NGO email from session
    ngo_email = session.get('ngo_email')
    
    if not ngo_email:
        flash('You need to be logged in as an NGO to send a friend request.', 'error')
        return redirect(url_for('login_ngo'))

    # Debug: Check if the NGO email is in the session
    print(f"[DEBUG] NGO Email from session: {ngo_email}")

    # Retrieve NGO details using the email
    ngo = ngos.find_one({"email": ngo_email})
    
    if not ngo:
        flash('NGO not found!', 'error')
        return redirect(url_for('login_ngo'))
    
    # Create friend request data
    request_data = {
        "ngo_email": ngo_email,
        "company_name": company_name,
        "status": "Pending"
    }

    # Assuming you have a collection to store friend requests
    friend_requests.insert_one(request_data)

    flash(f'Friend request sent to {company_name}!', 'success')
    return redirect(url_for('search_companies'))  # Redirect back to search page or wherever you want


@app.route('/ngo_friend_requests', methods=['GET'])
def ngo_friend_requests():
    ngo_name = session.get('ngo_name')  # Retrieve NGO name from session
    if not ngo_name:
        flash('You need to be logged in as an NGO.', 'error')
        return redirect(url_for('login'))

    # Find pending friend requests for this NGO by ngo_name
    requests = friend_requests.find({"ngo_name": ngo_name, "status": "Pending"})

    return render_template('ngo_requests.html', requests=requests)

@app.route('/friend_requests', methods=['GET'])
def view_friend_requests():
    company_email = session.get('company_email')  # Retrieve company email from session
    if not company_email:
        flash('Please log in as a company first!', 'error')
        return redirect(url_for('login_company'))

    # Check if the collection exists and fetch friend requests where the status is 'Pending'
    friend_requests = db['friend_requests'].find({"company_email": company_email, "status": "Pending"})

    # Debug: Print the friend requests to see if they're being retrieved correctly
    friend_requests_list = list(friend_requests)  # Convert cursor to a list for easier debugging
    

    # Render the friend requests page with the fetched data
    return render_template('friend_requests.html', friend_requests=friend_requests_list)


@app.route('/accept_request/<request_id>', methods=['POST'])
def accept_request(request_id):
    company_email = session.get('company_email')
    if not company_email:
        flash('Please log in as a company first!', 'error')
        return redirect(url_for('login_company'))
    company = db['companies'].find_one({"email": company_email})
    company_name = company.get('company_name')
    # Fetch the friend request from the database
    request = db['friend_requests'].find_one({"_id": ObjectId(request_id), "company_name": company_name})
    if not request:
        flash('Friend request not found!', 'error')
        return redirect(url_for('view_friend_requests'))
    

    # Update the request status to "Accepted"
    db['friend_requests'].update_one({"_id": ObjectId(request_id)}, {"$set": {"status": "Accepted"}})

    # Optionally: Add the company to the NGO's list of friends
    ngo_name = request['ngo_email']
    

    # Assuming ngo has a "friends" list (which is an array of company names)
    db['ngos'].update_one({"ngo_name": ngo_name}, {"$push": {"friends": company_name}})

    flash(f'You have accepted the friend request from {ngo_name}!', 'success')
    return redirect(url_for('view_friend_requests'))

@app.route('/friend_company_requests', methods=['GET'])
def view_friend_company_requests():
    company_email = session.get('company_email')  # Retrieve company email from session
    if not company_email:
        flash('Please log in as a company first!', 'error')
        return redirect(url_for('login_company'))

    # Retrieve the company_name using the company_email
    company = db['companies'].find_one({"email": company_email})
    if not company:
        flash('Company not found!', 'error')
        return redirect(url_for('login_company'))
    
    company_name = company['company_name']  # Extract company_name

    # Fetch the pending friend requests where the company_name matches and status is 'Pending'
    friend_requests = db['friend_requests'].find({
        "company_name": company_name,
        "status": "Pending"
    })

    # Convert cursor to a list for easier debugging and rendering
    friend_requests_list = list(friend_requests)

    # Debugging: print friend requests to confirm data
    print(f"[DEBUG] Retrieved Friend Requests: {friend_requests_list}")

    # Render the friend requests page with the fetched data
    return render_template('friend_requests_company.html', friend_requests=friend_requests_list)




def accept_request_company(request_id):
    if "company_email" not in session:
        flash("Please log in first!", "error")
        return redirect(url_for("login_company"))

    # Find the friend request by its ID
    request = db['friend_requests'].find_one({"_id": ObjectId(request_id)})

    if not request:
        flash("Friend request not found!", "error")
        return redirect(url_for('dashboard_company'))

    # Extract company_name and ngo_email from the request
    company_name = request["company_name"]
    ngo_email = request["ngo_email"]

    # Fetch company_email using company_name from the 'companies' collection
    company = db['companies'].find_one({"company_email": company_email})
    if not company:
        flash(f"Company {company_name} not found!", "error")
        return redirect(url_for('dashboard_company'))

    company_email = company.get("email")
    
    # Fetch ngo_name using ngo_email from the 'ngos' collection
    ngo = db['ngos'].find_one({"email": ngo_email})
    if not ngo:
        flash(f"NGO with email {ngo_email} not found!", "error")
        return redirect(url_for('dashboard_company'))

    ngo_name = ngo.get("ngo_name")

    # Debugging: print values before counterpart check
    print(f"Checking for counterpart with company_email: {company_email}, ngo_name: {ngo_name}")

    # Check if the counterpart exists (reverse request)
    counterpart = db['friend_requests'].find_one({
        "company_email": company_email,
        "ngo_name": ngo_name,
        "status": "Accepted"
    })

    if not counterpart:
        # Create the counterpart document
        counterpart_document = {
            "company_email": company_email,
            "ngo_name": ngo_name,
            "status": "Accepted"
        }

        # Insert the counterpart document into the friend_requests collection
        result = db['friend_requests'].insert_one(counterpart_document)

        # Debugging: confirm insertion
        print(f"Created counterpart: {counterpart_document}, inserted ID: {result.inserted_id}")

    # Now update the status of the original request to "Accepted"
    db['friend_requests'].update_one(
        {"_id": ObjectId(request_id)},
        {"$set": {"status": "Accepted"}}
    )

    # Update the company's and NGO's relationship (add them as friends)
    db['companies'].update_one(
        {"email": company_email},
        {"$push": {"friends": ngo_email}}
    )

    db['ngos'].update_one(
        {"email": ngo_email},
        {"$push": {"friends": company_email}}
    )

    flash("Friend request accepted!", "success")

    # Redirect back to the dashboard
    return redirect(url_for('dashboard_company'))






@app.route('/friends', methods=['GET'])
def view_friends():
    company_email = session.get('company_email')
    if not company_email:
        flash('Please log in as a company first!', 'error')
        return redirect(url_for('login_company'))

    # Get company details and retrieve the list of friends
    company = companies.find_one({"email": company_email})
    friends = company.get("friends", [])  # Assuming friends are stored in a 'friends' field

    # Debug: Print the friends to check the data
    print(f"[DEBUG] Company Friends: {friends}")

    return render_template('friends.html', friends=friends)

@app.route('/ngo/<ngo_name>')
def view_ngo(ngo_name):
    # Logic to handle the view of the NGO
    ngo = ngos.find_one({"name": ngo_name})
    return render_template("dashboard_ngo.html", ngo=ngo)



@app.route('/apply_collaborate/<event_name>', methods=['GET', 'POST'])
def apply_to_collaborate(event_name):
    # Fetch event details using the event name
    event = db.events.find_one({"event_name": event_name})
    if not event:
        return "Event not found!", 404

    if request.method == 'POST':
        # Handle the collaboration application
        if "ngo_email" not in session:
            return "Please log in first!", 403
        
        ngo = db.ngos.find_one({"email": session["ngo_email"]})
        if not ngo:
            return "NGO not found!", 404

        # Apply to collaborate with the event
        db.events.update_one(
            {"event_name": event_name},
            {"$addToSet": {"collaborators": ngo['ngo_name']}}  # Add NGO as collaborator
        )

        return redirect(url_for('apply_to_collaborate', event_name=event_name))  # Redirect to the same page

    return render_template('apply_collaboration.html', event=event)


@app.route('/logout')
def logout():
    session.pop("company_email", None)
    session.pop("ngo_email", None)
    flash("Logged out successfully!", "success")
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)
