from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super_secret_key_123")
# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["csr_database"]
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
        ngo_name = request.form['ngo_name']
        email = request.form['email']
        password = request.form['password']
        

        # Check if email already exists
        if ngos.find_one({"email": email}):
            flash("NGO Email already exists! Please login.", "error")
            return redirect(url_for("login_ngo"))

        # Store data in MongoDB
        ngo_data = {
            "ngo_name": ngo_name,
            "email": email,
            "password": password
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

        # Check if NGO exists
        ngo = ngos.find_one({"email": email})
        if ngo and check_password_hash(ngo["password"], password):
            session["ngo_email"] = email
            flash("NGO Login successful!", "success")
            return redirect(url_for("dashboard_ngo"))
        else:
            flash("Invalid NGO credentials. Try again!", "error")

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
    if "ngo_email" in session:
        return f"Welcome, {session['ngo_email']}! This is your NGO dashboard."
    flash("Please log in first!", "error")
    return redirect(url_for("login_ngo"))

@app.route('/dashboard/company')
def dashboard_company():
    if "company_email" in session:
        return f"Welcome, {session['company_email']}! This is your company dashboard."
    flash("Please log in first!", "error")
    return redirect(url_for("login_company"))

@app.route('/logout')
def logout():
    session.pop("company_email", None)
    session.pop("ngo_email", None)
    flash("Logged out successfully!", "success")
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)
