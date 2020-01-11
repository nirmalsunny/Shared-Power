import mysql.connector

def connect():
    mydb = mysql.connector.connect(
        host="remotemysql.com",
        user="1udfLy2lm1",
        passwd="1gxRoQC4vJ",
        database="1udfLy2lm1"
    )

    return mydb

def insert(query):
    # sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
    # val = ("John", "Highway 21")
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute(query)

    mydb.commit()

def select(query):
    # sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
    # val = ("John", "Highway 21")
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute(query)

    return mycursor.fetchall()
