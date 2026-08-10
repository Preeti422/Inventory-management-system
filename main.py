import pymysql
from database import conn
from customer import add_customer, view_customers
from product import add_product, view_products
from order import add_order, view_orders, add_order_item,view_order_items
from report import sales_report, customer_order_summary
while True:
    print("\n------ Inventory Order Management ------")
    print("1. Add Customer")
    print("2. View Customers")
    print("3. Add Products")
    print("4. View Products")
    print("5. Add Order")
    print("6. View Orders")
    print("7. Update Product Price")
    print("8. Delete Customer")
    print("9. Sales Report")
    print("10. Search Customer")
    print("11. Search Product")
    print("12. Low Stock Report")
    print("13. Total Sales")
    print("14. Add Order Items")
    print("15. View Order Items")
    print("16. Customer Order Summary")
    print("17. Exit")

    choice = input("Enter your choice: ")
    #ADD CUSTOMER 
    if choice == "1":
        add_customer()

    #VIEW CUSTOMERS   
    elif choice == "2":
        view_customers()

        
    #ADD PRODUCTS
    elif choice=="3":
        add_product()

    #VIEW PRODUCTS    
    elif choice=="4":
        view_products()

    #ADD ORDER
    elif choice=="5":
        add_order()

    #VIEW ORDERS    
    elif choice =="6":
       view_orders()

    #UPDATE PRODUCT PRICE
    elif choice=="7":
        product_id=int(input("Enter Product ID:"))
        new_price=float(input("Enter New Price:"))    

        if new_price <= 0:
            print("Price must be greater than 0!")
            continue

        cursor=conn.cursor()

        sql="""
        UPDATE Products 
        SET price=%s
        WHERE product_id=%s
        """

        cursor.execute(sql,(new_price,product_id))
        conn.commit()
        if cursor.rowcount > 0:
            print("Product Price Updated Successfully!")
        else:
            print("Product Not Found!")    

    #DELETE CUSTOMERS
    elif choice== "8":
       customer_id=input("Enter Customer ID to Delete:")
       cursor=conn.cursor()
       sql="DELETE FROM Customers WHERE customer_id=%s"


       try:
           cursor.execute(sql ,(customer_id,))
           conn.commit()
           if cursor.rowcount > 0:
               print("Customer Deleted Successfully!")
           else:
               print("Customer Not Found!")
       except pymysql.err.IntegrityError:
           print("Customer cannot be deleted because order exists for this customer.")  

    # SALES REPORT
    elif choice=="9":
        sales_report()                 

        
    #SEARCH CUSTOMER
        
    elif choice=="10":
        name=input("Enter Customer Name: ")
        cursor=conn.cursor()

        sql="""
        SELECT*FROM Customers
        WHERE name LIKE %s
        """
        cursor.execute(sql,("%"+ name+"%",))
        customers=cursor.fetchall()
        if customers:
            print("\n----CUSTOMER SEARCH RESULTS------")
            for customer in customers:
                print("Customer ID :", customer[0])
                print("Name   :", customer[1])
                print("Email  :", customer[2])
                print("Phone  :", customer[3])
                print("-"*40)
        else:
            print("Customer Not Found!")  

    #SEARCH PRODUCTS  
     
    elif choice=="11":
        product=input("Enter Product Name:")

        cursor=conn.cursor()

        sql="""
        SELECT*FROM Products
        WHERE product_name LIKE %s
        """
        cursor.execute(sql, ("%"+ product +"%",))
        products=cursor.fetchall()

        if products:
            print("\n-----PRODUCT SEARCH RESULTS-----")
            for row in products:
                print("Product ID  :", product[0])
                print("Product Name  :", product[1])
                print("Category      :", product[2])
                print("Price         :", product[3])
                print("Stock         :", product[4])
                print("-"*40)
                      
        else:
            print("Product Not Found!")

    #LOW STOCK REPORT

    elif choice=="12":
        cursor=conn.cursor()

        cursor.execute("""
        SELECT product_id,product_name,stock
        FROM Products
        WHERE stock < 10""")

        data=cursor.fetchall()

        print("\n------LOW STOCK REPORT-----")

        if data:
            for row in data:
                print("Product ID:", row[0])
                print("Product Name  :", row[1])
                print("Stock  :", row[2])
                print("-"*35)
        else: 
            print("No products are low in stock!")       

       
    #TOTAL SALES 

    elif choice=="13":
        cursor=conn.cursor()

        cursor.execute("""
        SELECT COALESCE(SUM(total_amount),0)
        FROM Orders
        """) 
        total=cursor.fetchone()
        if total is None:
            total=0

        print("Total Sales=",total[0]) 

    #ADD ORDER ITEM

    elif choice=="14":
      add_order_item()
    
    elif choice=="15":
       view_order_items()

    #CUSTOMER ORDER SUMMARY
    elif choice=="16":
        customer_order_summary()
        
    elif choice == "17":
        print("Thank You!")
        conn.close()
        break

    else:
        print("Invalid Choice")