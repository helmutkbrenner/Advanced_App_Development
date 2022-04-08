# Helmut Brenner #
# 2037275 #
# Dani Hargrove #
# 2037520 #
import mysql
from mysql.connector import Error


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        # checks for validity of the syntax, if valid then execute
        connection.commit()
        return 0
    except Error as e:
        print(f"The error '{e}' occurred.")
        return 1


def execute_read_query(connection, query):
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def connect():
    # this function just saves space and makes the code much cleaner.
    cnx = mysql.connector.connect(user='administrator', password='appleorange',
                                  host='cis3368.cbdmo6iefbst.us-east-2.rds.amazonaws.com', database='CIS3368DB')
    return cnx
