from database import conn


def sales_report():

    cursor = conn.cursor()

    sql = """
    SELECT
        c.name,
        p.product_name,
        oi.quantity,
        oi.price,
        (oi.quantity * oi.price) AS Total
    FROM Order_Items oi
    JOIN Orders o
        ON oi.order_id = o.order_id
    JOIN Customers c
        ON o.customer_id = c.customer_id
    JOIN Products p
        ON oi.product_id = p.product_id
    """

    cursor.execute(sql)

    data = cursor.fetchall()

    print("\n------ SALES REPORT ------")

    for row in data:
        print(row)


def customer_order_summary():

    cursor = conn.cursor()

    sql = """
    SELECT
        c.name,
        COUNT(DISTINCT o.order_id) AS Total_Orders,
        SUM(oi.quantity) AS Total_Items,
        SUM(oi.quantity * oi.price) AS Total_Spending
    FROM Customers c
    JOIN Orders o
        ON c.customer_id = o.customer_id
    JOIN Order_Items oi
        ON o.order_id = oi.order_id
    GROUP BY c.customer_id, c.name
    ORDER BY Total_Spending DESC
    """

    cursor.execute(sql)

    data = cursor.fetchall()

    print("\n------ CUSTOMER ORDER SUMMARY ------")

    for row in data:
        print(f"Customer: {row[0]}")
        print(f"Total Orders: {row[1]}")
        print(f"Total Items: {row[2]}")
        print(f"Total Spending: {row[3]}")
        