from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'vijaymvj110'
app.config['MYSQL_DB'] = 'productitems'

mysql = MySQL(app)

'''
@app.route('/create_table', methods=['POST'])
def create_table():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("CREATE TABLE items (id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(20),price FLOAT ,category "
                "VARCHAR(20))")
        cur.close()
        return jsonify({"MESSAGE": "Table created successfully"})
'''


@app.route('/add', methods=['POST'])
def create_product():
    with app.app_context():
        name = request.json['name']
        price = request.json['price']
        category = request.json['category']

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO items (name,price,category) VALUES (%s,%s,%s)", (name, price, category))
        mysql.connection.commit()
        cur.close()
        return jsonify({"Message": "Product created successfully"})


@app.route('/get', methods=['GET'])
def get_product():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM items")
        get = cur.fetchall()
        cur.close()

        items_list = []

        for getitems in get:
            product_dict = {'id': getitems[0], 'name': getitems[1], 'price': getitems[2], 'category': getitems[3]}
            items_list.append(product_dict)
        return jsonify(items_list)


if __name__ == '__main__':
    app.run(debug=True)
