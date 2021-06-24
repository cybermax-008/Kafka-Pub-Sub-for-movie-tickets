import json
import os
import time
from kafka import KafkaConsumer
import argparse
import helper

"""
Consumer script : This script is responsible for conencting with Aiven Kafka cluster and subscribing
movie ticket messages and storing in the database under the created table.
"""

def consumer_func(certName,hostName,portNumber,topicName,tableName):
    # setting up the connection with database
    db_conn = helper.set_connection()
    c = db_conn.cursor()
    # Create Kafka Consumer instance
    consumer = KafkaConsumer(
        bootstrap_servers=(hostName+":"+portNumber),
        auto_offset_reset='earliest',
        security_protocol="SSL",
        ssl_cafile=os.path.join(certName,"ca.pem"),
        ssl_certfile=os.path.join(certName,"service.cert"),
        ssl_keyfile=os.path.join(certName,"service.key"),
        consumer_timeout_ms=1000,
    )
    print("Kafka Consumer Instance is set subscribe data....")
    # subscribing to the topic of interest
    consumer.subscribe([topicName])

    # storing all messages in a list
    data = []
    for message in consumer:
        message = json.loads(message.value.decode("utf-8"))
        print("Recieved: {}".format(message))
        data.append(message)
    # inserting messages one by one to the table
    for msg in data:
        query = """
        INSERT INTO {}(ticket_id,theater,movie,seats,name,email,phone_number)
        VALUES ({},'{}','{}','{}','{}','{}','{}');
        """.format(tableName,
                   msg["id"],
                   str(msg["theater"]),
                   str(msg["movie"]),
                   ",".join(msg["seats"]),
                   str(msg["name"]),
                   str(msg["email"]),
                   str(msg["phone_number"]))
        c.execute(query)
    print("INSERTED THE MESSAGES IN DATABASE")
    c.close()
    db_conn.commit()
    db_conn.close()
    consumer.close()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cert-path',
                         help="Path that contains Aiven Kafka Certificates", 
                         required=True)
    parser.add_argument("--topic-name",
                        help="Topic name",
                        required=True)
    parser.add_argument("--table-name",
                        help="Name of the table to commit the data",
                        required=True)
    return parser.parse_args()

def main(args):
    # Get the kafka credentials
    cred_data =  helper.get_creds()[0]
    print("Loaded Aiven Kafka Authentication Credentials... ")

    # Setting up the crendential variables
    cert_path =  args.cert_path
    host_name = cred_data["KAFKA_HOST"]
    port_number = cred_data["KAFKA_PORT"]
    topic_name = args.topic_name
    table_name = args.table_name

    #Running the Consumer
    consumer_func(cert_path,
                  host_name,
                  port_number,
                  topic_name,
                  table_name
                  )

if __name__ == "__main__":
    args = parse_args()
    main(args)