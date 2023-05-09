import mysql.connector
from mysql.connector import Error
import json
with open("token.json", 'r') as raw_data:
    data = json.load(raw_data)

data = data["$schema"]


# FIXME: change mysql.connector to aiomysql
# because mysql.connector can't handle refreshing data 


def mysqlConnection():
    db_connection = None
    try:
        db_connection = mysql.connector.connect(**data)
    except Error as e:
        print(e)
    
    return db_connection


def mysqlQueryWithValue(query, value):
    connection = mysqlConnection()
    cursor = connection.cursor(buffered=False)
    data = None
    cursor.execute(query, value)
    data = cursor.fetchall()
    print('Query executed correcly!')
    connection.close()
    return data        
    
def mysqlQuery(query):
    connection = mysqlConnection()
    cursor = connection.cursor(buffered=False)
    data = None
    cursor.execute(query)
    data = cursor.fetchall()
    print('Query executed correcly!')
    connection.close()
    return data     
    

def mysqlQueryDeleteUpdateWithValue(query, value):
    connection = mysqlConnection()
    cursor = connection.cursor(buffered=False)
    cursor.execute(query, value)
    print('Query executed correcly!')
    connection.commit()
    connection.close()


def mysqlUpdate(query):
    connection = mysqlConnection()
    cursor = connection.cursor(buffered=False)
    cursor.execute(query)
    print('Query executed correcly!')
    connection.commit()
    connection.close()


def mysqlInsertWithValue(query, value):
    connection = mysqlConnection()
    cursor = connection.cursor(buffered=False)
    cursor.execute(query, value)
    connection.commit()
    connection.close()
    row = cursor.lastrowid
    return row

 
def mysqlInsert(query):
    connection = mysqlConnection()
    cursor = connection.cursor(buffered=False)
    cursor.execute(query)
    connection.commit()
    connection.close()
    row = cursor.lastrowid
    return row
