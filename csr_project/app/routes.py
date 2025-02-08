from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register/ngo')
def register_ngo():
    return render_template('register_ngo.html')

@app.route('/register/company')
def register_company():
    return render_template('register_company.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/ngo')
def login_ngo():
    return render_template('login_ngo.html')

@app.route('/login/company')
def login_company():
    return render_template('login_company.html')

@app.route('/dashboard/ngo')
def dashboard_ngo():
    return render_template('dashboard_ngo.html')

@app.route('/dashboard/company')
def dashboard_company():
    return render_template('dashboard_company.html')

if __name__ == '__main__':
    app.run(debug=True)
