import psycopg2
import helper
import argparse
"""
This script helps to create a table in the Aiven PostgreSQL database if not exits already.
Here, table name is taken as command line argument.
"""
def create_db(table_name):
    # setting up the connection with db
    db_conn = helper.set_connection()
    c = db_conn.cursor()
    # create the table with given table name
    try:
        # NEEDS IMPROVEMENT : the seats are stored as TEXT format, which could be stored in separate table.
        # Adding ticket_id as primary key 
        query = """
        CREATE TABLE IF NOT EXISTS {}(
            ticket_id INTEGER NOT NULL,
            theater VARCHAR(255) NOT NULL,
            movie VARCHAR(255) NOT NULL,
            seats TEXT NOT NULL,
            name VARCHAR(200) NOT NULL,
            email VARCHAR(300) NOT NULL,
            phone_number VARCHAR(30)
        )
        """.format(table_name)
        c.execute(query)
        print("Successfully created the table.")
        c.close()
        db_conn.commit()
    except (Exception, psycopg2.Error) as error:
        raise RuntimeError(f"Error setting up table for PG database: {error}")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--table-name",
                        help="Table name to be created to store data",
                        required=True)
    return parser.parse_args()

def main(args):
    table_name = args.table_name
    create_db(table_name)

if __name__ == "__main__":
    args = parse_args()
    main(args)