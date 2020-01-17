# Database Module for easier use of connection and queries
# mysql is a dependency. It has to be installed beforehand.

import mysql.connector


def connect():
    mydb = mysql.connector.connect(
        host="remotemysql.com",
        user="1udfLy2lm1",
        passwd="1gxRoQC4vJ",
        database="1udfLy2lm1"
    )

    return mydb

# For any update queries


def insert(query):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute(query)

    mydb.commit()

# For any queries that returns a result


def select(query):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute(query)

    return mycursor.fetchall()
