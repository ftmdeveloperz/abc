from flask import Flask, request, redirect, url_for, render_template, flash
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your actual secret key
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'funtoonsmultimedia@gmail.com'
app.config['MAIL_PASSWORD'] = 'ftm@2024'  # Directly use your password here
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)

s = URLSafeTimedSerializer('your_secret_key')  # Replace with your actual secret key

# Define your User class
class User(UserMixin):
    # User model logic goes here
    pass

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        # Save user to database
        otp_secret = 'your_otp_secret'
        send_otp(email, otp_secret)
        flash('A verification email has been sent!', 'info')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Verify user credentials
        return redirect(url_for('profile'))
    return render_template('login.html')

@app.route('/post', methods=['POST'])
@login_required
def post():
    content = request.form['content']
    # Save post to database
    flash('Post created!', 'success')
    return redirect(url_for('profile'))

@app.route('/profile')
@login_required
def profile():
    # Fetch user posts and data
    return render_template('profile.html')

@app.route('/send-test-email')
def send_test_email():
    msg = Message('Test Email', sender='funtoonsmultimedia@gmail.com', recipients=['recipient@example.com'])
    msg.body = 'This is a test email sent from Flask.'
    try:
        mail.send(msg)
        return 'Email sent successfully!'
    except Exception as e:
        return f'Error: {str(e)}'

def send_otp(email, otp_secret):
    token = s.dumps(email, salt='email-confirm')
    msg = Message('Your OTP Code', sender='funtoonsmultimedia@gmail.com', recipients=[email])
    msg.body = f'Your OTP code is {otp_secret}'
    try:
        mail.send(msg)
    except Exception as e:
        print(f'Error sending OTP: {str(e)}')

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return 'The token has expired!'
    # Confirm user email
    return 'Email confirmed!'

if __name__ == '__main__':
    app.run(debug=True)
