import psycopg2
import helper
"""
This script helps to drop a table in the Aiven PostgreSQL database if exits already.
Here, table name is taken as command line argument.
"""
def drop_tables():
    # setting up the connection with db
    db_conn = helper.set_connection()
    c = db_conn.cursor()
    try:
        #select all tables in the current database
        query = """
        SELECT table_name FROM information_schema.tables
        WHERE table_schema ='public';
        """
        c.execute(query)
        result = c.fetchone()
        if result:
            for table in result:
                q = """
                DROP TABLE IF EXISTS {} 
                """.format(table)
                print(f"Successfully dropped the table : {table}.")
                c.execute(q)
        else:
            print("No tables available to be dropped!")
        c.close()
        db_conn.commit()
    except (Exception, psycopg2.Error) as error:
        raise RuntimeError(f"Error dropping the table: {error}")

def main():
    drop_tables()

if __name__ == "__main__":
    main()