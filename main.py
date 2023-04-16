from tabulate import tabulate
import mysql.connector

con = mysql.connector.connect(host="localhost", user="root", password="vijaymvj110", database="python_db")


def insert(name, age, city, gender):
    res = con.cursor()
    sql = "insert into users_list (name, age, city,gender) values (%s,%s,%s,%s)"
    user = (name, age, city, gender)
    res.execute(sql, user)
    con.commit()
    print("Data insert success")


def update(name, age, city, gender, id):
    res = con.cursor()
    sql = "update users_list set name=%s,age=%s,city=%s,gender=%s where id=%s"
    user = (name, age, city, gender, id)
    res.execute(sql, user)
    con.commit()
    print("Data update success")


def select():
    res = con.cursor()
    sql = "SELECT ID,NAME,AGE,CITY,GENDER from users_list"
    res.execute(sql)
    result = res.fetchall()
    print(tabulate(result, headers=['id', 'name', 'age', 'city', 'gender']))


def delete(id):
    res = con.cursor()
    sql = "Delete from users_list where id=%s"
    user = (id,)
    res.execute(sql, user)
    con.commit()
    print("Data delete success")


while True:
    print("1.Insert Data")
    print("2.Update Data")
    print("3.Select Data")
    print("4.Delete data")
    print("5.Exit")
    choice = int(input("Enter your choice:"))
    if choice == 1:
        name = input("Enter name:")
        age = input("Enter age:")
        city = input("Enter city:")
        gender = input("Enter gender:")
        insert(name, age, city, gender)
    elif choice == 2:
        id = int(input("Enter ID:"))
        name = input("Enter name:")
        age = input("Enter age:")
        city = input("Enter city:")
        gender = input("Enter gender:")
        update(name, age, city,  gender, id)
    elif choice == 3:
        select()
    elif choice == 4:
        id = input("Enter Id to Delete:")
        delete(id)
    elif choice == 5:
        quit()
    else:
        print("Invalid selection. please try again")
