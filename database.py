import pymysql

conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="Preeti123",
    database="ecommerce",
    port=3307
)

print("Database Connected Successfully!")