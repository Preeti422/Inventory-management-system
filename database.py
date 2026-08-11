import pymysql
import os

conn = pymysql.connect(
    host=os.environ.get("TIDB_HOST"),
    user=os.environ.get("TIDB_USER"),
    password=os.environ.get("TIDB_PASSWORD"),
    database=os.environ.get("TIDB_DATABASE"),
    port=4000
)

print("Database Connected Successfully")