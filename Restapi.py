from flask import Flask, json, jsonify, request
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

db = SQLAlchemy()
ma = Marshmallow()

mysql = MySQL(app)


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(10), nullable=False)

    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category


class ProductSchema(ma.Schema):
    class meta:
        fields = ("id", "name", "price", "category")


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:vijaymvj110@localhost/productitems"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///Database.db"
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/add', methods=['POST'])
def add_product():
    _json = request.json
    name = _json['name']
    price = _json['price']
    category = _json['category']
    new_product = Items(name=name, price=price, category=category)
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"Message": "Your product has been added"})


@app.route('/get', methods=['GET'])
def get_product():
    data = Items.query.all()
    products = products_schema.dump(data)
    return jsonify(products)


@app.route("/get/<id>", methods=["GET"])
def product_byid(id):
    if str.isdigit(id) == False:
        return jsonify(f"Message:ID of the product cannot be a string")
    else:
        data = []
        product = Items.query.get(id)
        if product is None:
            return jsonify(f"No products was found")
        data = product_schema.dump(product)
        return jsonify(data)


@app.route('/product/delete/<id>', methods=["POST"])
def delete_byid(id):
    product = Items.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify(f"The product has been deleted")


if __name__ == '__main__':
    app.run(debug=True)
