import json
import os
import time
from kafka import KafkaProducer
from faker import Faker
import argparse
import random
from FakeMovieTicket import TicketGen
import helper
"""
Producer script : This script is responsible for conencting with Aiven Kafka cluster and publishing the fake
movie tickets generated.
"""

# Max tickets an user can buy
MAX_TICKETS = 10


def book_ticket(ticket_id = 1):
    # create a movie ticket message with generated fake informations.
    new_ticket = TicketGen(ticket_id)
    theater = new_ticket.theater()
    name,email,phone_number = new_ticket.userInfo()
    movie = new_ticket.movieName()
    seat_list = [new_ticket.seats() for i in range(0,random.randint(1,MAX_TICKETS+1))]

    key = {"id":ticket_id}
    message = {
        "id":ticket_id,
        "theater":theater,
        "movie":movie,
        "name":name,
        "email":email,
        "phone_number":phone_number,
        "seats":seat_list
    }
    return key, message



def producer_func(certName,hostName,portNumber,topicName,numberOfMessages,test =False):
    # Create Kafka Producer instance  
    producer = KafkaProducer(
        bootstrap_servers=(hostName+":"+portNumber),
        security_protocol="SSL",
        ssl_cafile=os.path.join(certName,"ca.pem"),
        ssl_certfile=os.path.join(certName,"service.cert"),
        ssl_keyfile=os.path.join(certName,"service.key"),
        value_serializer=lambda v: json.dumps(v).encode('ascii'),
        key_serializer=lambda v: json.dumps(v).encode('ascii')
    )
    print("Kafka Producer Instance is set publish data....")

    #Generate and publish data to kafka topic
    try:
        if test:
            numberOfMessages = random.randint(200,800)
            msg = numberOfMessages
        else:
            numberOfMessages = int(numberOfMessages)
            msg = 0
        while(msg <= numberOfMessages):
            key,message = book_ticket(msg)
            print("Sending: {}".format(message))
            producer.send(topicName,
                        key=key,
                        value=message)
            time.sleep(2)

            if msg == numberOfMessages:
                producer.flush()
            msg+=1
        producer.flush()
        print("Message published Successfully! ")
    except Exception as e:
        raise(f"Error sending the message:{e}")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cert-path',
                         help="Path that contains Aiven Kafka Certificates", 
                         required=True)
    parser.add_argument("--topic-name",
                        help="Topic name",
                        required=True)
    parser.add_argument("--num",
                        help="Number of messages to be produced",
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
    num_of_msgs = args.num

    #Running the Producer
    producer_func(cert_path,
                  host_name,
                  port_number,
                  topic_name,
                  num_of_msgs
                  )

if __name__ == "__main__":
    args = parse_args()
    main(args)
    
