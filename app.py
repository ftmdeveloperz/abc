from flask import Flask, request, render_template, redirect, url_for, flash
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'funtoonsmultimedia@gmail.com'
app.config['MAIL_PASSWORD'] = 'ftm@2023'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Dummy user class for demonstration
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_otp_via_email(email, otp_code):
    msg = Message('Your OTP Code', sender='your_email@gmail.com', recipients=[email])
    msg.body = f'Your OTP code is {otp_code}'
    mail.send(msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        otp_code = generate_otp()
        send_otp_via_email(email, otp_code)
        flash('A verification code has been sent to your email!', 'info')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        otp_code = request.form['otp_code']
        # Here you should validate the OTP code
        login_user(User(email))
        return redirect(url_for('profile'))
    return render_template('login.html')

@app.route('/profile')
@login_required
def profile():
    return f'Hello, {current_user.id}!'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # Change port to 8080
