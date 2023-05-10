from flask import Flask,jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost/products"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///Database.db"

db = SQLAlchemy(app)
ma = Marshmallow(app)


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
    class Meta:
        fields = ("id", "name", "price", "category")


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

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
    return jsonify({"Message": f"{name},{price} and {category} for Your product has been added"})


@app.route('/get', methods=['GET'])
def get_productitems():
    get_product = Items.query.all()
    result = products_schema.dump(get_product)
    return jsonify(result)


@app.route("/get/<id>", methods=["GET"])
def product_byid(id):
    if not str.isdigit(id):
        return jsonify(f"Message:ID of the product cannot be a string")
    else:
        product = Items.query.get(id)
        if product is None:
            return jsonify(f"No products was found for id = {id}")
        data = product_schema.dump(product)
        return jsonify(data)


@app.route('/update/<id>', methods=['PUT'])
def updateItem(id):
    _json = request.json
    name = _json['name']
    price = _json['price']
    category = _json['category']
    update = Items.query.get(id)
    if update is None:
        return jsonify(f"No items available for id = {id}")
    update.name=name
    update.price=price
    update.category=category
    db.session.commit()
    return jsonify({"Message":f"{id} th Item has been updated successfully"})


@app.route('/delete/<id>', methods=["POST"])
def delete_byid(id):
    product = Items.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify(f"The id = {id} product has been deleted successfully")


if __name__ == '__main__':
    app.run(debug=True)
