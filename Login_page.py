from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/login'
db = SQLAlchemy(app)


class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30, collation='utf8_bin'), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=True, unique=True)

    def __repr__(self):
        return f"Login({self.username})"


with app.app_context():
    # db.drop_all()
    db.create_all()


@app.route('/create_user', methods=['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']
    hashed_password = generate_password_hash(password)

    if not username and not password:
        return jsonify({'Message': 'Username and password field should not be a empty'}), 400

    if not username:
        return jsonify({'Message': 'Username should not be empty'}), 400

    if not password:
        return jsonify({'Message': 'Password should not be empty'}), 400

    if not username.strip() or not password.strip():
        return jsonify({'Message': 'Empty spaces not allowed'}), 400

    if Login.query.filter_by(username=username).first():
        return jsonify({'Message': f'Username {username} is already exists!.Try again.'}), 409

    new_user = Login(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'Message': f'Username {username} is created successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    user = Login.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'Message': 'Invalid User name or password'}), 401
    return jsonify({'Message': 'Login successful'}), 200


if __name__ == '__main__':
    app.run(debug=True)
