from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Setup Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  # or 465 for SSL
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'funtoonsmultimedia@gmail.com'
app.config['MAIL_PASSWORD'] = '6206213510'
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)

users = {}
otp_secrets = {}
posts = []

class User(UserMixin):
    def __init__(self, username, password, email):
        self.id = username
        self.password = generate_password_hash(password)
        self.email = email
        self.following = set()

@login_manager.user_loader
def load_user(username):
    return users.get(username)

@app.route('/')
def index():
    return render_template('index.html', posts=posts, user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if username not in users:
            user = User(username, password, email)
            users[username] = user
            otp_secret = pyotp.random_base32()
            otp_secrets[username] = otp_secret
            send_otp(email, otp_secret)
            session['register_user'] = username
            return redirect(url_for('verify_otp'))
        else:
            flash('User already exists', 'error')
    return render_template('register.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        username = session.get('register_user')
        otp = request.form['otp']
        secret = otp_secrets.get(username)
        if pyotp.TOTP(secret).verify(otp):
            return redirect(url_for('login'))
        else:
            flash('Invalid OTP', 'error')
    return render_template('verify_otp.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/post', methods=['POST'])
@login_required
def post():
    content = request.form['content']
    post_id = len(posts)
    posts.append({
        'id': post_id,
        'content': content,
        'author': current_user.id,
        'likes': set(),
        'comments': []
    })
    return redirect(url_for('index'))

@app.route('/like/<int:post_id>')
@login_required
def like(post_id):
    if 0 <= post_id < len(posts):
        post = posts[post_id]
        if current_user.id not in post['likes']:
            post['likes'].add(current_user.id)
        else:
            post['likes'].remove(current_user.id)
    return redirect(url_for('index'))

@app.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def comment(post_id):
    if 0 <= post_id < len(posts):
        content = request.form['comment']
        posts[post_id]['comments'].append({
            'author': current_user.id,
            'content': content
        })
    return redirect(url_for('index'))

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = users.get(username)
    if user and user.id != current_user.id:
        current_user.following.add(user.id)
    return redirect(url_for('index'))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = users.get(username)
    if user and user.id != current_user.id:
        current_user.following.discard(user.id)
    return redirect(url_for('index'))

def send_otp(email, otp_secret):
    otp = pyotp.TOTP(otp_secret).now()
    msg = Message('Your OTP Code', sender='your_email@example.com', recipients=[email])
    msg.body = f'Your OTP code is {otp}.'
    mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True)
