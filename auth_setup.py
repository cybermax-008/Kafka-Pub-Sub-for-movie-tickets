import os
import argparse
import json
# command line args parsing
parser = argparse.ArgumentParser()
parser.add_argument("--kafka-hostname",
                    help="Host name of Aiven kafka service available in Avien.io console",
                    required=True)
parser.add_argument("--kafka-portnumber",
                    help="port number of aiven kafka service available in Avien.io console",
                    required=True)
parser.add_argument("--postgres-uri",
                    help="The POSTGRES_URI config variable available in Avien.io console",
                    required=True)
args = parser.parse_args()

credentials = [{"KAFKA_HOST":args.kafka_hostname,
                "KAFKA_PORT":args.kafka_portnumber,
                "POSTGRES_URI":args.postgres_uri}]
# file that stores these authetication variables 
filename = "creds.json"

with open(filename,"w") as f:
    json.dump(credentials,f)
