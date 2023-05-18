from flask import Flask, request
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
import mysql.connector

app = Flask(__name__)
auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Bearer')

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='Auth'
)

cursor = db.cursor()

table_exists_query = "SHOW TABLES LIKE 'authorization'"
cursor.execute(table_exists_query)
table_exist = cursor.fetchall()

user_exists_query = "SHOW TABLES LIKE 'user'"
cursor.execute(user_exists_query)
user_exist = cursor.fetchall()

if not table_exist:
    create_table_query = "CREATE TABLE authorization (id INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR (255))"
    cursor.execute(create_table_query)

    create_user_query = "CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR (255))"
    cursor.execute(create_user_query)

users = {
    "saran": "pass",
    "alice": "password"
}

tokens = {
    "naveen_token": "john",
    "alice_token": "alice"
}


@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username


@token_auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]


@app.route('/protected/basic')
@auth.login_required()
def protected_basic():
    username = auth.current_user()
    query = "INSERT INTO users (username) VALUES (%s)"
    cursor.execute(query, (username,))
    db.commit()
    return f"Hello,{username} ! This is the protected route with basic authentication."


@app.route('/protected/token')
@token_auth.login_required()
def protected_token():
    username = token_auth.current_user()
    query = "INSERT INTO users (username) VALUES (%s)"
    cursor.execute(query, (username,))
    db.commit()
    return f"Hello,{username} ! This is the protected route with token authentication."


if __name__ == '__main__':
    app.run(debug=True)
