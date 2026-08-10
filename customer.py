import pymysql
from database import conn


def add_customer():

    name = input("Enter Name: ")
    email = input("Enter Email: ")
    phone = input("Enter Phone: ")
    city = input("Enter City: ")
    password = input("Enter Password: ")

    cursor = conn.cursor()

    sql = """
    INSERT INTO Customers(name, email, phone, city, password)
    VALUES(%s, %s, %s, %s, %s)
    """

    try:
        cursor.execute(sql, (name, email, phone, city, password))
        conn.commit()
        print("Customer Added Successfully!")

    except pymysql.err.IntegrityError:
        print("Email already exists! Please use another email.")


def view_customers():

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Customers")

    data = cursor.fetchall()

    print("\n------ CUSTOMERS ------")

    for row in data:
        print("Customer ID  :", row[0])
        print("Name   :", row[1])
        print("Email  :", row[2])
        print("Phone  :", row[3])
        print("City   :", row[4])
        print("-"*40)