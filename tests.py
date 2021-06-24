import psycopg2
import helper
import argparse
from producer import producer_func
from consumer import consumer_func
import random
from db_setup import create_db
from drop_tables import drop_tables

"""
This test scripts contains methods that tests individual components of the pipeline.
"""

parser = argparse.ArgumentParser()
parser.add_argument('--cert-path',
                        help="Path that contains Aiven Kafka Certificates", 
                        required=True)

args = parser.parse_args()
# Setting up the crendential variables
CERT_PATH =  args.cert_path

# Demo variables to be used for testing
random_num = str(random.randint(0,5000))
TEST_TOPIC= "test_topic" + random_num
TEST_TABLE = 'test_table'

# Kakfa and Postgres authentication credentials
cred_data =  helper.get_creds()[0]
HOST_NAME = cred_data["KAFKA_HOST"]
PORT_NUMBER = cred_data["KAFKA_PORT"]

def table_existence_test():
    # setting up the connection with db
    db_conn = helper.set_connection()
    c = db_conn.cursor()
    try:
        # query to check if the table exists
        query = """
        SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_schema ='public'
        AND table_name = '{}'
        )
        """.format(TEST_TABLE)

        c.execute(query)
        result = c.fetchone()
        if result[0]:
            print("#### TEST PASSED FOR TABLE EXISTENCE COMPLETED ####")
        else:
            print("#### TEST FAILED: FOR TABLE EXISTENCE COMPLETED ####")
        c.close()
        db_conn.close()
    except (Exception, psycopg2.Error) as error:
        raise RuntimeError(f"Error Query: {error}")
        print("#### TEST FAILED: FOR TABLE EXISTENCE COMPLETED ####")
    

def table_data_test():
    # setting up the connection with db
    db_conn = helper.set_connection()
    c = db_conn.cursor()
    try:
        # query to check if the table exists
        query = """
        SELECT * FROM {} 
        ORDER BY ticket_id DESC LIMIT 1
        """.format(TEST_TABLE)

        c.execute(query)
        result = c.fetchone()
        if result:
            print(f"The last row of the table {TEST_TABLE} :\n{result}")
            print("#### TEST PASSED: FOR TABLE DATA EXISTENCE COMPLETED ####")
        else:
            print(f"There is no data available inside {TEST_TABLE} table")
            print("#### TEST FAILED: FOR TABLE DATA EXISTENCE COMPLETED ####")
        c.close()
        db_conn.close()
    except (Exception, psycopg2.Error) as error:
        raise RuntimeError(f"Error Query: {error}")
        print("#### TEST FAILED: FOR TABLE DATA EXISTENCE COMPLETED ####")

def table_creation_test():
    create_db(TEST_TABLE)

def producer_test():
    # producer instance for sending one test message to test topic
    producer_func(CERT_PATH,
                           HOST_NAME,
                           PORT_NUMBER,
                           TEST_TOPIC,
                           1,
                           test=True)

def consumer_test():
     # consumer instance for getting test messages from test topic
    consumer_func(CERT_PATH,
                           HOST_NAME,
                           PORT_NUMBER,
                           TEST_TOPIC,
                           TEST_TABLE)
    
def main():
    print("SELECT THE TEST TO BE PERFORMED:\n"
          "1. Test if the producer is able to publish messages to the Kafka topic\n"
          "2. Test for table creation in the database\n"
          "3. Test the table existence in PostgreSQL database\n"
          "4. Test if the consumer is able to subscribe and store the data to PostgreSQL database\n"
          "5. Test if the data is stored in the database\n"
          "6. Run all tests!\n"
          "7. Exit the Test suite!")
    while True:
        selection = input("-->")
        if selection == "1":
            producer_test()
        elif selection == "2":
            table_creation_test()
        elif selection == "3":
            table_existence_test()
        elif selection == "4":
            consumer_test()
        elif selection == "5":
            table_data_test()
        elif selection =="6":
            print("Running All tests...")
            drop_tables()
            producer_test()
            table_creation_test()
            table_existence_test()
            consumer_test()
            table_data_test()
            print("ALL TESTS COMPLETED SUCESSFULLY!")
        elif selection == "7":
            print("Exiting the test suite! Thank You!")
            break
        else:
            print("Give the right test selection!")


if __name__ == "__main__":
    main()