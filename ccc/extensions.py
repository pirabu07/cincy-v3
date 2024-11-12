import pymysql
import mysql.connector


def get_db():
    """
    Establishes a connection to the MySQL database and returns the connection object.

    Returns:
        conn (pymysql.connections.Connection): The connection object to the MySQL database.
    """
    # mysql connection
    conn = None
    try:
        # conn = pymysql.connect(
        #     host='localhost',
        #     database='ccc',
        #     user='root',
        #     password='root',
        #     cursorclass=pymysql.cursors.DictCursor
        # )

        conn = mysql.connector.connect(
            host='localhost',
            database='ccc',
            user='root',
            password='root'
        )
    except pymysql.Error as e:
        print(e)
    # finally:
    #     if conn is not None:
    #         conn.close()
    return conn


# list_cursor = db.cursor()
# dict_cursor = db.cursor(MySQLdb.cursors.DictCursor)
