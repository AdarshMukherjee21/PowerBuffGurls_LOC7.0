from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/company/signup')
def company_signup():
    return render_template('company_signup.html')

@app.route('/ngo/signup')
def ngo_signup():
    return render_template('ngo_signup.html')

@app.route('/company/login')
def company_login():
    return render_template('company_login.html')

@app.route('/ngo/login')
def ngo_login():
    return render_template('ngo_login.html')

if __name__ == '__main__':
    app.run(debug=True)