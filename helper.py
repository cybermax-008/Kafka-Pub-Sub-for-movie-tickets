import os
import json
import psycopg2
"""
This is helper code that is being used in producer.py , consumer.py and db_setup.py.
1. For getting the authentication crednetials from the creds.json file
2. setting the a connection with postgreSQL db.
"""
def get_creds():
    # Get crendentials from creds.json and return as dictionary
    try:
        data_file = open("creds.json", "r")
        data = json.loads(data_file.read())
        return data
    except IOError as e:
        raise RuntimeError("Error Parsing the JSON file: {}".format(e))

def set_connection():
    # Initiating a connection with database using postgreSQL URI
    uri = get_creds()[0]["POSTGRES_URI"]
    try:
        db_conn = psycopg2.connect(uri)
        return db_conn
    except Exception as e:
        raise RuntimeError(f"Error connecting to the database: {e}")