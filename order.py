import pymysql 
from database import conn


def add_order():

    order_id = int(input("Enter Order ID: "))
    customer_id = int(input("Enter Customer ID: "))
    order_date = input("Enter Order Date: ")
    total_amount = float(input("Enter Total Amount: "))
    if total_amount < 0:
        print("Total amount cannot be negative!")
        return

    cursor = conn.cursor()

    sql = """
    INSERT INTO Orders(order_id, customer_id, order_date, total_amount)
    VALUES(%s, %s, %s, %s)
    """

    try:
        cursor.execute(
        sql,
        (order_id, customer_id, order_date, total_amount)
        )

        conn.commit()

        print("Order Added Successfully!")

    except pymysql.err.IntegrityError:
        print("Order ID already exists or Customer ID is invalid!")    


def view_orders():

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Orders")

    orders = cursor.fetchall()

    print("\n------ ORDERS ------")

    for order in orders:
         print("Order ID     :", order[0])
         print("Customer ID  :", order[1])
         print("Order Date   :", order[2])
         print("Total Amount :", order[3])
         print("-" * 40)

def add_order_item():

    order_id = int(input("Enter Order ID: "))
    product_id = int(input("Enter Product ID: "))
    quantity = int(input("Enter Quantity: "))

    if quantity <= 0:
        print("Quantity must be greater than 0!")
        return

    cursor = conn.cursor()
    cursor.execute(
        "SELECT order_id FROM Orders WHERE order_id = %s",
        (order_id,)
    )

    order=cursor.fetchone()
    if order is None:
        print("Order Not Found!")
        return
    
    cursor.execute(
        "SELECT stock, price FROM Products WHERE product_id = %s",
        (product_id,)
    )

    product = cursor.fetchone()

    if product is None:
        print("Product Not Found!")
        return

    stock = product[0]
    price = product[1]

    if quantity > stock:
        print("Not Enough Stock!")
        return

    sql = """
    INSERT INTO Order_Items(order_id, product_id, quantity, price)
    VALUES(%s, %s, %s, %s)
    """

    cursor.execute(
        sql,
        (order_id, product_id, quantity, price)
    )

    cursor.execute(
        """
        UPDATE Products
        SET stock = stock - %s
        WHERE product_id = %s
        """,
        (quantity, product_id)
    )

    conn.commit()

    print("Order Item Added Successfully!")
    print("Stock Updated Successfully!")        

def view_order_items():

    cursor = conn.cursor()

    sql = """
    SELECT
        oi.order_id,
        p.product_name,
        oi.quantity,
        oi.price,
        (oi.quantity * oi.price) AS total
    FROM Order_Items oi
    JOIN Products p
    ON oi.product_id = p.product_id
    """

    cursor.execute(sql)

    items = cursor.fetchall()

    print("\n------ ORDER ITEMS ------")

    if items:
        for item in items:
            print("Order ID     :", item[0])
            print("Product Name :", item[1])
            print("Quantity     :", item[2])
            print("Price        :", item[3])
            print("Total        :", item[4])
            print("-" * 40)
    else:
        print("No Order Items Found!")