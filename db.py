import mysql.connector

def get_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='api-gpt'
        )
        print("Connection successful.")
        return conn
    except mysql.connector.Error as err:
        print(f"Connection failed: {err}")
        return None