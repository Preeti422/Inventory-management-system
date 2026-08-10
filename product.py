import pymysql
from database import conn


def add_product():

    product_name = input("Enter Product Name: ")
    price = float(input("Enter Price: "))
    stock = int(input("Enter Stock: "))
    category_id = int(input("Enter Category ID: "))
    if price <= 0:
        print("Price must be greater than 0!")
        return
    if stock < 0:
        print("Stock Cannot be negative!")
        return
   
    cursor = conn.cursor()

    sql = """
    INSERT INTO Products (product_name, price, stock, category_id)
    VALUES (%s, %s, %s, %s)
    """

    try:
        cursor.execute(sql, (product_name, price, stock, category_id))
        conn.commit()

        print("Product Added Successfully!")

    except pymysql.err.IntegrityError:
        print("Product already exists or invalid category!")


def view_products():

    cursor = conn.cursor()

    cursor.execute("SELECT*FROM Products")

    products = cursor.fetchall()

    for product in products:
        print("Product ID  :", product[0])
        print("Product Name :",product[1])
        print("Price  :", product[2])
        print("Stock  :", product[3])
        print("Category ID  :",product[4])
        print("_"*40)