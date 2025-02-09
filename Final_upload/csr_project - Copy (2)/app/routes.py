from flask import Flask, render_template, request, redirect, url_for, session, flash,jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
from app.matching_algorithm import match_ngos_for_company
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
    ngos = []
    
    if request.method == "POST":
        search_query = request.form.get("search_query", "").strip()
        if search_query:
            ngos = list(db.ngos.find({"ngo_name": {"$regex": search_query, "$options": "i"}}))

    return render_template("search_ngos.html", ngos=ngos)








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

@app.route('/match_event')
def match_event():
    if "ngo_email" not in session:
        return "Please log in first!", 403

    ngo = db.ngos.find_one({"email": session["ngo_email"]})
    if not ngo:
        return "NGO not found!", 404

    # Get events from the NGO's document
    upcoming_events = ngo.get("events", [])

    return render_template("match_event.html", ngo=ngo, upcoming_events=upcoming_events)

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

@app.route('/match_company')
def match_company():
    # Route logic
    return render_template("match_company.html")


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
    print(f"[DEBUG] Retrieved Friend Requests: {friend_requests_list}")

    # Render the friend requests page with the fetched data
    return render_template('friend_requests.html', friend_requests=friend_requests_list)


@app.route('/accept_request/<request_id>', methods=['POST'])
def accept_request(request_id):
    company_email = session.get('company_email')
    if not company_email:
        flash('Please log in as a company first!', 'error')
        return redirect(url_for('login_company'))

    # Fetch the friend request from the database
    request = db['friend_requests'].find_one({"_id": ObjectId(request_id), "company_email": company_email})
    if not request:
        flash('Friend request not found!', 'error')
        return redirect(url_for('view_friend_requests'))

    # Update the request status to "Accepted"
    db['friend_requests'].update_one({"_id": ObjectId(request_id)}, {"$set": {"status": "Accepted"}})

    # Optionally: Add the company to the NGO's list of friends
    ngo_name = request['ngo_name']
    company_name = companies.find_one({"email": company_email})['company_name']

    # Assuming ngo has a "friends" list (which is an array of company names)
    db['ngos'].update_one({"ngo_name": ngo_name}, {"$push": {"friends": company_name}})

    flash(f'You have accepted the friend request from {ngo_name}!', 'success')
    return redirect(url_for('view_friend_requests'))


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

@app.route('/match_company_for_event/<event_name>')
def match_company_for_event(event_name):
    if "ngo_email" not in session:
        return "Please log in first!", 403

    ngo = db.ngos.find_one({"email": session["ngo_email"]})
    if not ngo:
        return "NGO not found!", 404

    # Get the event details from the NGO's events list
    event = next((e for e in ngo['events'] if e['event_name'] == event_name), None)
    if not event:
        return "Event not found!", 404

    # Get a list of matching companies (example function call)
    matches = match_companies_for_ngo(ngo["ngo_name"], event)  # Adjust matching function for event
    session["company_matches"] = matches
    session["current_company_index"] = 0

    return render_template("match_companies_for_event.html", event_name=event_name)

@app.route('/next_company_for_event/<event_name>')
def next_company_for_event(event_name):
    if "ngo_email" not in session:
        return "Please log in first!", 403

    ngo = db.ngos.find_one({"email": session["ngo_email"]})
    if not ngo:
        return "NGO not found!", 404

    matches = match_company_for_event(event_name)  # Call the matching algorithm based on the event
    session["company_matches"] = matches
    session["current_company_index"] = 0

    return jsonify({"company": matches[session["current_company_index"]][0], "score": matches[session["current_company_index"]][1]})

@app.route('/like_company_for_event', methods=['POST'])
def like_company_for_event():
    if "ngo_email" not in session:
        return "Unauthorized", 403

    data = request.json
    company_name = data.get("company_name")
    event_name = data.get("event_name")

    # Add the liked company to the event's collaborators list
    db.ngos.update_one(
        {"email": session["ngo_email"], "events.event_name": event_name},
        {"$addToSet": {"events.$.collaborators": company_name}}
    )

    return jsonify({"status": "liked"})

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
