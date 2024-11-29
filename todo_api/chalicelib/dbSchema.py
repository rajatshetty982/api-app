import psycopg2
from chalicelib.dbConnections import getDbConnection
from chalice import Response

def create_table():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS todos (
        id SERIAL PRIMARY KEY,
        task TEXT NOT NULL,
        start_date DATE DEFAULT CURRENT_DATE,
        end_date DATE,
        status TEXT DEFAULT 'Pending'
    );
    """

    # Establishing the connection and creating the schema

    try:
        conn = getDbConnection()
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        conn.commit()
        conn.close()
        reponseMessage = {'message': "Schema created successfully!"}
        return Response(body=reponseMessage, status_code=200, headers={'Content-Type': 'application/json'})
    
    except Exception as e:
        return Response(body={'error': str(e)}, status_code=500, headers={'Content-Type': 'application/json'})

    finally:
            conn.close()
