import mysql.connector
from mysql.connector import Error
import json
<<<<<<< HEAD


=======
>>>>>>> 50dcec8 (.)
with open("token.json", 'r') as raw_data:
    data = json.load(raw_data)

data = data["$schema"]


<<<<<<< HEAD
def mysql_connection() -> mysql.connector.MySQLConnection | None:
    r'''Connects to MySQL database with parameters already defined in a json config file.
        
        Returns
        -----------
        db_connection: :class:`MySQLConnection`
            Connection to the database.
        
        Raises
        -----------
        mysql.connector.Error
            When connection fails.
    '''
    db_connection = None
    try:
        db_connection: mysql.connector.MySQLConnection = mysql.connector.connect(**data)
=======
# FIXME: change mysql.connector to aiomysql
# because mysql.connector can't handle refreshing data 


def mysqlConnection():
    db_connection = None
    try:
        db_connection = mysql.connector.connect(**data)
>>>>>>> 50dcec8 (.)
    except Error as e:
        print(e)
    
    return db_connection


<<<<<<< HEAD
def mysql_query_with_value(query: str, value: tuple) -> tuple | None:
    r'''Executes MySQL query with given values.
    
        Parameters
        -----------
        query: :class:`str`
            Query that will be exectued.
        value: class:`tuple`
            Values given to the query.
        
        Returns
        -----------
        data: :class:`tuple` | :class:`None`
            Row containing row's data in tuple.
        
        Raises
        -----------
        mysql.connector.Error
            When connection fails.
    '''
    connection: mysql.connector.MySQLConnection = mysql_connection()
    cursor = connection.cursor(buffered=False)
    data = None
    cursor.execute(query, value)
    data: tuple = cursor.fetchone()
    connection.close()
    return data        
    
    
def mysql_query(query: str) -> tuple | None:
    r'''Read the data from MySQL database.
    
        Parameters
        -----------
        query: :class:`str`
            Query that will be executed.
        
        Returns
        -----------
        data: :class:`tuple` | :class:`None`
            Row containing row's data in tuple.
        
        Raises
        -----------
        mysql.connector.Error
            When connection fails.
    '''
    connection: mysql.connector.MySQLConnection = mysql_connection()
    cursor = connection.cursor(buffered=False)
    data = None
    cursor.execute(query)
    data: tuple = cursor.fetchone()
=======
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
>>>>>>> 50dcec8 (.)
    connection.close()
    return data     
    

<<<<<<< HEAD
def mysql_query_delete_update_with_value(query: str, value: tuple) -> None:
    r'''
        Parameters
        -----------
        query: :class:`str`
            Query that will be exectued.
        value: class:`tuple`
            Values given to the query.
            
        Raises
        -----------
        mysql.connector.Error
            When connection fails.
    '''
    connection: mysql.connector.MySQLConnection = mysql_connection()
    cursor = connection.cursor(buffered=False)
    cursor.execute(query, value)
=======
def mysqlQueryDeleteUpdateWithValue(query, value):
    connection = mysqlConnection()
    cursor = connection.cursor(buffered=False)
    cursor.execute(query, value)
    print('Query executed correcly!')
>>>>>>> 50dcec8 (.)
    connection.commit()
    connection.close()


<<<<<<< HEAD
def mysql_update(query: str) -> None:
    r'''Updates already existing rows in MySQL database.
        
        Parameters
        -----------
        query: :class:`str`
            Query that will be exectued.
            
        Raises
        -----------
        mysql.connector.Error
            When connection fails.
    '''
    connection: mysql.connector.MySQLConnection = mysql_connection()
    cursor = connection.cursor(buffered=False)
    cursor.execute(query)
=======
def mysqlUpdate(query):
    connection = mysqlConnection()
    cursor = connection.cursor(buffered=False)
    cursor.execute(query)
    print('Query executed correcly!')
>>>>>>> 50dcec8 (.)
    connection.commit()
    connection.close()


<<<<<<< HEAD
def mysql_insert_with_value(query: str, value: tuple) -> int | None:
    r'''
        Parameters
        -----------
        query: :class:`str`
            Query that will be exectued.
        value: class:`tuple`
            Values given to the query.
            
        Returns
        -----------
        row: :class:`int` | :class:`None`
            Value generated for the auto-increment column.
        
        Raises
        -----------
        mysql.connector.Error
            When connection fails.
    '''
    connection: mysql.connector.MySQLConnection = mysql_connection()
    cursor = connection.cursor(buffered=False)
    cursor.execute(query, value)
    row: int | None = cursor.lastrowid
    connection.commit()
    connection.close()
    return row

 
def mysql_insert(query) -> int | None:
    r'''
        Parameters
        -----------
        query: :class:`str`
            Query that will be exectued.
            
        Returns
        -----------
        row: :class:`int` | :class:`None`
            Value generated for the auto-increment column.
            
        Raises
        -----------
        mysql.connector.Error
            When connection fails.
    '''
    connection: mysql.connector.MySQLConnection = mysql_connection()
    cursor = connection.cursor(buffered=False)
    cursor.execute(query)
    connection.commit()
    row: int | None = cursor.lastrowid
    connection.close()
    return row
   
=======
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
>>>>>>> 50dcec8 (.)
