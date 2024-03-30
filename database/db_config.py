import mysql.connector
from mysql.connector import Error
from datetime import datetime

from sqlalchemy import create_engine

# Replace the user, password, host, port, and dbname with your details
#DATABASE_URI = 'mysql+pymysql://akshat:possible@mysql:3306/YoutubeData'

#engine = create_engine(DATABASE_URI)


def get_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='mysql',  # or your host, e.g., '127.0.0.1'
            database='YouTubeData',  # your database name
            user='root',  # your mysql username
            password='possible'
            )  # your mysql password
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
    return connection

