from flask import Flask, render_template,request,redirect,session
from database import conn

app = Flask(__name__)
app.secret_key="inventory-secret-key"

@app.route("/")
def home():
    if "username" not in session:
        return redirect("/login")
    return render_template("index.html")

@app.route("/customers",methods=["GET","POST"])
def customers():
    if "username" not in session:
        return redirect("/login")
    cursor = conn.cursor()

    
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        city = request.form["city"]
        password = request.form["password"]

    
        sql="""
        INSERT INTO Customers(name,email,phone,city,password)
        VALUES(%s,%s,%s,%s,%s)
        """

        cursor.execute(sql , (name,email,phone,city,password))
        conn.commit()
        
    
    cursor.execute("""
    SELECT customer_id,name,email,phone,city
    FROM Customers
    """)

    customers=cursor.fetchall()
    print("CUSTOMERS FROM DATABASE:",customers)
    return render_template("customer.html",customers=customers)

@app.route("/products", methods=["GET","POST"])
def products():
    if "username" not in session:
        return redirect("/login")

    cursor=conn.cursor()
    
    if request.method=="POST":

        product_name = request.form["product_name"]
        price = float(request.form["price"])
        if price < 0:
         return "Price cannot be negative!"
        stock = int(request.form["stock"])
        if price < 0:
         return "Price cannot be negative!"
        category_id = request.form["category_id"]

        sql="""
        INSERT INTO Products(product_name,price,stock,category_id)
        VALUES(%s,%s,%s,%s)
        """
        cursor.execute(sql,(product_name,price,stock,category_id))
        conn.commit()
    cursor.execute("""
    SELECT product_id,product_name,price,stock,category_id
    FROM Products
    """)

    products=cursor.fetchall()
    return render_template("product.html",products=products)  

@app.route("/orders", methods=["GET","POST"])
def orders():
    if "username" not in session:
        return redirect("/login")
    cursor=conn.cursor()
    if request.method=="POST":
        customer_id = request.form["customer_id"]
        order_date = request.form["order_date"]

        cursor.execute(
        "SELECT customer_id FROM Customers WHERE customer_id=%s",
         (customer_id,)
         )
        customer = cursor.fetchone()

        if customer is None:
         return "Customer Not Found!"
       

        sql="""
        INSERT INTO Orders(customer_id,order_date,total_amount)
        VALUES(%s,%s,%s)
        """
        cursor.execute(sql,(customer_id,order_date,0))
        conn.commit()

    cursor.execute("SELECT*FROM Orders")
    orders=cursor.fetchall()
    return render_template("order.html",orders=orders)

@app.route("/order_items",methods=["GET","POST"])
def order_items():
    if"username" not in session:
        return redirect("/login")
    cursor=conn.cursor()
    if request.method=="POST":
        order_id=request.form["order_id"]
        product_id=request.form["product_id"]
        quantity=int(request.form["quantity"])
        #Quantity check
        if quantity <= 0:
            return"Quantity must be greater than 0!"

        #Check order
        cursor.execute("SELECT order_id FROM Orders WHERE order_id=%s",(order_id,))
        order=cursor.fetchone()

        if order is None:
            return "Order Not Found!"

        #Check Product And Get stock + price
        cursor.execute("SELECT stock,price FROM Products WHERE product_id=%s",(product_id,))
        product =cursor.fetchone()

        if product is None:
            return "Product Not Found!"
        stock=product[0]
        price=product[1]

        #Check Stock
        if quantity > stock:
            return "Not Enough Stock!"
        #Add Order Item
        sql="""
        INSERT INTO Order_Items(order_id,product_id,quantity,price)
        VALUES(%s,%s,%s,%s)
        """
        cursor.execute(sql,(order_id,product_id,quantity,price))

        #Reduce Stock
        cursor.execute(
        """
        UPDATE Products
        SET stock = stock-%s
        WHERE product_id=%s 
        """,
        (quantity,product_id)

        )

        # Update Order Total Amount
        cursor.execute("""
        UPDATE Orders
        SET total_amount = (
        SELECT COALESCE(SUM(quantity * price), 0)
        FROM Order_Items
        WHERE order_id = %s
        )
        WHERE order_id = %s
        """, (order_id, order_id))
        conn.commit()

        #Show Order Items
    sql="""
    SELECT 
    oi.order_items_id,
    oi.order_id,
    p.product_name,
    oi.quantity,
    oi.price,
    (oi.quantity*oi.price) AS Total
    FROM Order_Items oi
    JOIN Products p
    ON oi.product_id=p.product_id
    """

    cursor.execute(sql)
    items=cursor.fetchall()
    return render_template("order_item.html",items=items)

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/login")

    cursor=conn.cursor()

    #Total Sales
    cursor.execute("""
    SELECT COALESCE(SUM(total_amount),0)
    FROM Orders
    """
    )
    total_sales=cursor.fetchone()[0]

    #Total Orders
    cursor.execute("""
    SELECT COUNT(*)
    FROM Orders
    """)
    total_orders=cursor.fetchone()[0]

    #Total Customers
    cursor.execute("""
    SELECT COUNT(*)
    FROM Customers
    """)
    total_customers=cursor.fetchone()[0]

    #Total Products
    cursor.execute("""
    SELECT COUNT(*)
    FROM Products
    """)
    total_products=cursor.fetchone()[0]

    return render_template("dashboard.html",
    total_sales=total_sales,
    total_orders=total_orders,
    total_customers=total_customers,
    total_products=total_products)

@app.route("/low_stock")
def low_stock():
    if "username" not in session:
     return redirect("/login")

    cursor = conn.cursor()

    sql = """
    SELECT product_id, product_name, price, stock
    FROM Products
    WHERE stock < 10
    """

    cursor.execute(sql)

    products = cursor.fetchall()

    return render_template("low_stock.html", products=products)

@app.route("/search_customer", methods=["GET","POST"])
def search_customer():
    if "username" not in session:
     return redirect("/login")
    customers=[]
    searched=False

    if request.method=="POST":
        name=request.form["name"]
        cursor=conn.cursor()

        sql="""
        SELECT customer_id,name,email,phone,city
        FROM Customers
        WHERE name LIKE %s
        """
        cursor.execute(sql,("%"+name+"%",))

        customers=cursor.fetchall()
        searched=True
    return render_template("search_customer.html",customers=customers,searched=searched)

@app.route("/search_product", methods=["GET", "POST"])
def search_product():
    if "username" not in session:
     return redirect("/login")

    products = []
    searched = False

    if request.method == "POST":

        product_name = request.form["name"]

        cursor = conn.cursor()

        sql = """
        SELECT product_id, product_name, price, stock, category_id
        FROM Products
        WHERE product_name LIKE %s
        """

        cursor.execute(
            sql,
            ("%" + product_name + "%",)
        )

        products = cursor.fetchall()

        searched = True

    return render_template(
        "search_product.html",
        products=products,
        searched=searched
    )

@app.route("/update_product/<int:product_id>", methods=["GET","POST"])
def update_product(product_id):
    if "username" not in session:
        return redirect("/login")

    cursor=conn.cursor()
    if request.method=="POST":

        product_name = request.form["product_name"]
        price = request.form["price"]
        stock = request.form["stock"]
        category_id = request.form["category_id"]

        sql = """
        UPDATE Products
        SET product_name=%s,
        price=%s,
        stock=%s,
        category_id=%s
        WHERE product_id=%s
        """
        cursor.execute(sql ,(product_name,price,stock,category_id,product_id))

        conn.commit()
        return "Product Updated Successfuly!"

    cursor.execute(
        "SELECT*FROM Products WHERE product_id=%s",
        (product_id,)
    )

    product=cursor.fetchone()
    print("PRODUCT:", product)
    return render_template("update_product.html", product=product)

@app.route("/delete_product/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    if "username" not in session:
        return redirect("/login")

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM Products WHERE product_id=%s",
        (product_id,)
    )

    conn.commit()

    return "Product Deleted Successfully!"

@app.route("/update_customer/<int:customer_id>", methods=["GET", "POST"])
def update_customer(customer_id):
    if "username" not in session:
        return redirect("/login")

    cursor = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        city = request.form["city"]
        password = request.form["password"]

        sql = """
        UPDATE Customers
        SET name=%s,
            email=%s,
            phone=%s,
            city=%s,
            password=%s
        WHERE customer_id=%s
        """

        cursor.execute(
            sql,
            (name, email, phone, city, password, customer_id)
        )

        conn.commit()

        return "Customer Updated Successfully!"

    cursor.execute(
        "SELECT * FROM Customers WHERE customer_id=%s",
        (customer_id,)
    )

    customer = cursor.fetchone()

    return render_template(
        "update_customer.html",
        customer=customer
    )

@app.route("/delete_customer/<int:customer_id>", methods=["POST"])
def delete_customer(customer_id):
    if "username" not in session:
        return redirect("/login")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM Orders WHERE customer_id=%s",
        (customer_id,)
    )

    order_count = cursor.fetchone()[0]

    if order_count > 0:
        return "Customer cannot be deleted because existing orders are linked to this customer!"

    cursor.execute(
        "DELETE FROM Customers WHERE customer_id=%s",
        (customer_id,)
    )

    conn.commit()

    return "Customer Deleted Successfully!"

@app.route("/sales_report")
def sales_report():
    if "username" not in session:
        return redirect("/login")

    cursor = conn.cursor()

    sql = """
    SELECT
    o.order_id,
    o.order_date,
    c.name,
    p.product_name,
    oi.quantity,
    oi.price,
    (oi.quantity * oi.price) AS total_amount
FROM Orders o
JOIN Customers c
    ON o.customer_id = c.customer_id
JOIN Order_Items oi
    ON o.order_id = oi.order_id
JOIN Products p
    ON oi.product_id = p.product_id
ORDER BY o.order_date DESC
"""
    cursor.execute(sql)

    sales = cursor.fetchall()

    # Total Sales
    cursor.execute("""
        SELECT COALESCE(SUM(quantity * price), 0)
        FROM Order_Items
    """)

    total_sales = cursor.fetchone()[0]

    return render_template(
        "sales_report.html",
        sales=sales,
        total_sales=total_sales
    )

@app.route("/edit_order_items/<int:id>", methods=["GET","POST"])
def edit_order_items(id):
    if "username" not in session:
        return redirect("/login")

    cursor=conn.cursor()
    if request.method=="POST":
        quantity=int(request.form["quantity"])

        if quantity <= 0:
            return"Quantity must be greater than 0!"

        #Get Current Order Item
        cursor.execute("""
        SELECT order_id,product_id,quantity
        FROM Order_Items
        WHERE order_items_id = %s
        """,(id,))

        item=cursor.fetchone()

        if item is None:
            return "Order Item Not Found!"
        order_id = item[0]
        product_id = item[1]
        old_quantity = item[2]

        #Difference in Quantity
        difference = quantity - old_quantity

        #Get product stock and price
        cursor.execute("""
        SELECT stock,price
        FROM Products
        WHERE product_id=%s
        """,(product_id,))

        product=cursor.fetchone()
        stock = product[0]
        price = product[1]

        # If increasing quantity
        if difference > stock:
            return "Not Enough Stock!"

        # Update Order Item
        cursor.execute("""
            UPDATE Order_Items
            SET quantity = %s,
                price = %s
            WHERE order_items_id = %s
        """, (quantity, price, id))

        # Adjust stock
        cursor.execute("""
            UPDATE Products
            SET stock = stock - %s
            WHERE product_id = %s
        """, (difference, product_id))

         # Update Order Total
        cursor.execute("""
            UPDATE Orders
            SET total_amount = (
                SELECT COALESCE(SUM(quantity * price), 0)
                FROM Order_Items
                WHERE order_id = %s
            )
            WHERE order_id = %s
        """, (order_id, order_id))

        conn.commit()

        return redirect("/order_items")

    # GET → show current item
    cursor.execute("""
        SELECT order_items_id, order_id, product_id, quantity, price
        FROM Order_Items
        WHERE order_items_id = %s
    """, (id,))

    item = cursor.fetchone()

    return render_template("edit_order_item.html", item=item)

@app.route("/delete_order_item/<int:id>", methods=["POST"])
def delete_order_item(id):
    if "username" not in session:
        return redirect("/login")

    cursor = conn.cursor()

    # current order information
    cursor.execute("""
        SELECT order_id, product_id, quantity
        FROM Order_Items
        WHERE order_items_id = %s
    """, (id,))

    item = cursor.fetchone()

    if item is None:
        return "Order Item Not Found!"

    order_id = item[0]
    product_id = item[1]
    quantity = item[2]

    # Add stock of product
    cursor.execute("""
        UPDATE Products
        SET stock = stock + %s
        WHERE product_id = %s
    """, (quantity, product_id))


    # Delete Order Item
    cursor.execute("""
        DELETE FROM Order_Items
        WHERE order_items_id = %s
    """, (id,))

    # Recalculate total order
    cursor.execute("""
        UPDATE Orders
        SET total_amount = (
            SELECT COALESCE(SUM(quantity * price), 0)
            FROM Order_Items
            WHERE order_id = %s
        )
        WHERE order_id = %s
    """, (order_id, order_id))

    conn.commit()

    return redirect("/order_items")

@app.route("/edit_order/<int:id>", methods=["GET", "POST"])
def edit_order(id):
    if "username" not in session:
        return redirect["/login"]

    cursor = conn.cursor()

    if request.method == "POST":

        customer_id = request.form["customer_id"]
        order_date = request.form["order_date"]

        cursor.execute("""
            UPDATE Orders
            SET customer_id = %s,
                order_date = %s
            WHERE order_id = %s
        """, (customer_id, order_date, id))

        conn.commit()

        return redirect("/orders")

    cursor.execute("""
        SELECT order_id, customer_id, order_date
        FROM Orders
        WHERE order_id = %s
    """, (id,))

    order = cursor.fetchone()

    if order is None:
        return "Order Not Found!"

    return render_template("edit_order.html", order=order)

@app.route("/delete_order/<int:id>", methods=["POST"])
def delete_order(id):
    if "username" not in session:
        return redirect("/login")

    cursor = conn.cursor()

    # Check order exist or not
    cursor.execute("""
        SELECT order_id
        FROM Orders
        WHERE order_id = %s
    """, (id,))

    order = cursor.fetchone()

    if order is None:
        return "Order Not Found!"

    # Order Item delete 
    cursor.execute("""
        DELETE FROM Order_Items
        WHERE order_id = %s
    """, (id,))
    

    # Order delete 
    cursor.execute("""
        DELETE FROM Orders
        WHERE order_id = %s
    """, (id,))

    conn.commit()

    return redirect("/orders")
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cursor.fetchone()

        if user:
            session["username"] = username
            return redirect("/dashboard")

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")


    

                       
                       
                       




  

if __name__ == "__main__":
    app.run(debug=True)