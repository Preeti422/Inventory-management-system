import pymysql

conn = pymysql.connect(
    host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    user="38jWyBcVqEC9YEJ.root",
    password="lXL7ciUwZsBByfC0",
    database="ecommerce",
    port=4000
)

print("Database Connected Successfully")