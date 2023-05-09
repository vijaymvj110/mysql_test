from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
# print(basedir)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    contact = db.Column(db.Integer, unique=True)

    def __init__(self, name, contact):
        self.name = name
        self.contact = contact


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'contact')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

with app.app_context():
    db.create_all()


@app.route('/user', methods=['POST'])
def add_user():
    name = request.json['name']
    contact = request.json['contact']
    new_user = User(name, contact)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)


@app.route('/user', methods=['GET'])
def get_all_user():
    all_user = User.query.all()
    result = users_schema.dump(all_user)
    return jsonify(result)


@app.route('/user/<id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


@app.route('/user/<id>', methods=['PUT'])
def update_user_by_id(id):
    update_user = User.query.get(id)
    name = request.json['name']
    contact = request.json['contact']
    update_user.name = name
    update_user.contact = contact
    db.session.commit()
    return user_schema.jsonify(update_user)


@app.route('/user/<id>', methods=['DELETE'])
def delete_by_id(id):
    delete_user = User.query.get(id)
    db.session.delete(delete_user)
    db.session.commit()
    return user_schema.jsonify(delete_user)


if __name__ == '__main__':
    app.run(debug=True)
