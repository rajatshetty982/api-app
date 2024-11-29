import os
import psycopg2

DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

db_connection = None

def getDbConnection():

    global db_connection
    
    if db_connection is None:
        db_connection = psycopg2.connect(user=DB_USER,password=DB_PASSWORD,host=DB_HOST,port=DB_PORT,database=DB_NAME)

    return db_connection
