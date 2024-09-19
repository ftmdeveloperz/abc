from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
import pyotp
import os

app = Flask(__name__)

# Configuration for email (update these with your actual details)
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your-email@example.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# OTP setup
otp = pyotp.TOTP('base32secret3232')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    otp_code = otp.now()
    msg = Message('Your OTP Code', sender='your-email@example.com', recipients=[email])
    msg.body = f'Your OTP code is {otp_code}'
    mail.send(msg)
    return jsonify({'message': 'OTP sent to your email!'})

@app.route('/verify', methods=['POST'])
def verify():
    email = request.form['email']
    code = request.form['code']
    if otp.verify(code):
        return jsonify({'message': 'Verification successful!'})
    else:
        return jsonify({'message': 'Invalid OTP code.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))