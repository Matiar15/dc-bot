import mysql.connector
from mysql.connector import Error
from datetime import datetime


config = {
'user': 'x687',
'password': '8699_b06082',
'host': 'mysql.mikr.us',
'database': 'db_x687',
'raise_on_warnings': True,}


def mysqlConnection():
    db_connection = None
    try:
        db_connection = mysql.connector.connect(**config)
    except Error as e:
        print(e)
    
    return db_connection


def mysqlQuery(connection, query, value):
    cursor = connection.cursor(buffered=False)
    data = None
    cursor.execute(query, value)
    data = cursor.fetchall()
    print('Query executed correcly!')
    return data        
    

def mysqlQueryForDelete(connection, query, value):
    cursor = connection.cursor(buffered=False)
    cursor.execute(query, value)
    print('SQL DELETE executed correcly!')
    connection.commit()
    

def mysqlInsertWithValue(connection, query, value):
    cursor = connection.cursor(buffered=False)
    cursor.execute(query, value)
    connection.commit()
    row = cursor.lastrowid
    return row


def mysqlInsert(connection, query):
    cursor = connection.cursor(buffered=False)
    cursor.execute(query)
    connection.commit()
    row = cursor.lastrowid
    return row
    

def mysqlUpdateWithValue(connection, query, value):
    cursor = connection.cursor(buffered=False)
    cursor.execute(query, value)
    print('SQL UPDATE executed correcly!')
    connection.commit()


def mysqlUpdate(connection, query):
    cursor = connection.cursor(buffered=False)
    cursor.execute(query)
    print('SQL UPDATE executed correcly!')
    connection.commit()


def checkConnection(connection):
    if not connection.is_connected:
        return mysqlConnection()
    else:
        return connection

