from flask import Flask
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Gmail SMTP configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'funtoonsmultimedia@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Use an environment variable for security
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

@app.route('/send-test-email')
def send_test_email():
    msg = Message('Test Email', sender='funtoonsmultimedia@gmail.com', recipients=['recipient@example.com'])
    msg.body = 'This is a test email sent from Flask.'
    try:
        mail.send(msg)
        return 'Email sent successfully!'
    except Exception as e:
        return f'Error: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
