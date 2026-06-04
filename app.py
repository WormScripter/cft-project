
from flask import Flask, render_template, request, session, redirect, url_for
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_SECRET_KEY"


def get_db():
    return psycopg2.connect(
        host="aws-1-ap-southeast-2.pooler.supabase.com",
        database="postgres",
        user="postgres",
        password="#HelloWorld809",
        port="5432",
        sslmode="require"
    )


# Home Page
@app.route('/')
def index():
    return render_template('index.html')


# Login Page
@app.route('/login-page')
def login_page():
    return render_template('login.html')


# Signup Page
@app.route('/signup-page')
def signup_page():
    return render_template('sigup.html')


# Dashboard
@app.route('/dashboard')
def dashboard():

    if 'username' not in session:
        return redirect(url_for('login_page'))

    return render_template(
        'dashboard.html',
        username=session['username']
    )


# Login Process
@app.route('/login', methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE username=%s",
        (username,)
    )

    user = cursor.fetchone()

    cursor.close()
    db.close()

    if user and check_password_hash(user[0], password):
        session['username'] = username
        return redirect(url_for('dashboard'))

    return "Invalid Username or Password"


# Signup Process
@app.route('/signup', methods=['POST'])
def signup():

    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        return "Passwords do not match"

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username=%s",
        (username,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        db.close()
        return "Username already exists"

    hashed_password = generate_password_hash(password)

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, hashed_password)
    )

    db.commit()

    cursor.close()
    db.close()

    session['username'] = username

    return redirect(url_for('dashboard'))


# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)

