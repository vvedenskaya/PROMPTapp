from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message 
import random
import string

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'promptgramm.app@gmail.com'
app.config['MAIL_PASSWORD'] = 'ishe wxdz jzqh vbtz'
app.config['MAIL_USE_SSL'] = True

db = SQLAlchemy(app)
mail = Mail(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    token = db.Column(db.String(120), unique=True, nullable=False)


with app.app_context(): 
    db.create_all()

def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))


@app.route('/')
def index():
    return render_template('testerReg.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']

    if User.query.filter_by(email=email).first():
        return jsonify({"success": "false", "message": "Can't create new user. User with this email already exists"}), 400
    
    token = generate_token()
    new_user = User(name=name, email=email, confirmed=False, token=token)
    db.session.add(new_user)
    db.session.commit()

    msg = Message('Confirm your registration', sender='promptgramm.app@gmail.com', recipients=[email])
    confirmation_url = url_for('confirm', id=new_user.id, token=token, _external=True)
    msg.body = f"Please click the link to confirm your registration: {confirmation_url}"
    mail.send(msg)

    return jsonify({"success": "true", "message": "Check your email to finish registration"}),200

@app.route('/confirm', methods=['GET'])
def confirm():
    user_id = request.args.get('id')
    token = request.args.get('token')

    user = User.query.get(user_id)

    if user and user.token == token:
        user.confirmed = True
        db.session.commit()
        return render_template('emailConfirm.html')
    else:
        return jsonify({"success": "false", "message": "Invalid token or user"}), 400


@app.route('/status', methods=['GET'])
def status():
    user_id = request.args.get('id')
    user = User.query.get(user_id)

    if user:
        return jsonify({"success": "true", "message": "User found", "user": {"name": user.name, "email": user.email, "confirmed": user.confirmed}})
    else:
        return jsonify({"success": "false", "message": "User not found"}), 404

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    user_id = data.get('id')
    token = data.get('token')

    user = User.query.get(user_id)

    if user and user.token == token:
        user.confirmed = True
        db.session.commit()
        return jsonify({"success": "true", "message": "User confirmed"}), 200
    else:
        return jsonify({"success": "false", "message": "Invalid token or user"}), 400
    

if __name__ == '__main__':
    app.run(debug=True)