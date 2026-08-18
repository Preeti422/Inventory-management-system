import pymysql
import os

conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password=os.getenv("DB_PASSWORD"),
    database="ecommerce",
    port=3307
)