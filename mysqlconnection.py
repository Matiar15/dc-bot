import mysql.connector
from mysql.connector import Error
import json


with open("token.json", 'r') as raw_data:
    data = json.load(raw_data)

data = data["$schema"]
print(data)

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
    except Error as e:
        print(e)
    
    return db_connection


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
    connection.close()
    return data     
    

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
    connection.commit()
    connection.close()


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
    connection.commit()
    connection.close()


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
   