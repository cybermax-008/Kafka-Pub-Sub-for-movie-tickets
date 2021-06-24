# Kafka Application: Publish/Subscribe Movie tickets
## Description
This is a Kafka application that uses Aiven Kafka service and Aiven PostgreSQL service. The objective is to publish randomly generated fake movie tickets(JSON message) using a producer fucntion to a Kafka topic which is created on Aiven Kafka service. Then, a consumer fucntion will subscribe on Kafka service and load those messages and finally pushing them to PostgreSQL database that is also hosted on Aiven PostgreSQL service.

## Aiven service setup
For this project,  we can leverage Aiven services in order to use `kafka` cluster and `postgreSQL` database. Aiven provides one month trial on signing up for Aiven account. It provides free 300$ credit for new users, in order to create and try out their services. To register and start with, visit [https://console.aiven.io/signup.html](https://console.aiven.io/signup.html). After signing up, you can access all services in the account dashboard [https://console.aiven.io/project](https://console.aiven.io/project).

For this project, we can create two services : `Kafka` and `PostgreSQL`.

**`Aiven Kafka`**

Create a new service and config the following settings as follows:
- Kafka Version 2.7
- GCP 
- us-east4
- Service plan : Business-4
- provide a service name (optional, else taken by default)

Once the service is created, it can be powered ON for use. For using the service for the program,
1. Note down the `SERVICE URI` (We will use in later part)
2. Download three certificates : `CA Cert` , `Access Key` and `Access Cert` in a desired directory but not the project directory(for security reasons). These are required for valid authentication while connecting the service from local.

**`Aiven PostgreSQL`**

Create a new service and config the following settings as follows:
- PostgreSQL v12.6
- GCP
- us-east4
- Service plan : Business-4
- provide a service name (optional, else taken by default)

Just, Note down the `SERVICE URI` for secure authentication from local.

## Installation & Pre-requisites
This application rely on,
1. `Python 3.5` and above
2. `Faker` module
3. `Kafka`v(2.7)
4. `postgreSQL`v(12.6)

The installation of necessary libraries are given in `requirements.txt`.

1. To start with, Run the code below to install all required libraries,

```bash
pip install -r requirements.txt
```

2. Run `auth_setup.py` to create `creds.json` that stores `SERVICE URI` of Kafka and postgresSQL. (Available at aiven console "Overview" tab)

```bash
python auth_setup.py --kafka-hostname kafka-<name>
                     --kafka-portnumber 11341
                     --postgres-uri <service-uri>
```
Where
- `kafka-hostname`  the Kafka host
- `kafka-portnumber` the Kafka port
- `postgres-uri` the postgres service URI

all of these are available at aiven service console.

## Running the application
3. Run `db_setup.py` to create the table in the `default db` in PostgreSQL.

```bash
python db_setup.py --table-name <movie_ticket>
```
This script connects to the `default db` and creates a `movie_ticket` table with following columns,
- `ticket_id` : unique ticket of each generated ticket. Eg: `<2>`
- `theater` : Name of the theater. Eg: `<Theater B>`
- `movie` : Name of the movie. Eg: `<The Forbidden Kingdom>`
- `name` : user name who is booking the ticket. Eg: `<John Nash>`
- `email` : email of the user. Eg: `<john.nash@gmail.com>`
- `phone_number` : phone number of the user. Eg: `<+1-891-646-2484>`
- `seats` : string of seat numbers seperated by comma. Eg: `<'Y2', 'Z10', 'G8', 'F9', 'Y3', 'I9', 'M4', 'W3'>`

4. Run `producer.py` to generate fake movie tickets and publish it to a topic in Kafak cluster at Aiven console.

```bash
python producer.py --cert-path <./Downloads>
                   --topic-name <movie_app>
                   --num <4>
```
5. Run `consumer.py` to subscribe for messages on the Kafka topic and store the messages in to PostgreSQL database. (Inside the table that we created)

```bash
python consumer.py --cert-path <./Downloads>
                   --topic-name <movie_app>
                   --table-name <movie_ticket>
```
Where,
- `cert-path` Path of the directory in which all certificates are saved.
- `topic-name` The topic name on to which we publish the messages.
- `num` the total number of messages to be generated and published.
- `table-name` table name on which we store the messages after consumed by the consumer app.

## Tests
The `tests.py` contains all the tests to be performed for this applcaition. There are totally 5 tests available for evaluation.
```bash
1. Test if the producer is able to publish messages to the Kafka topic
2. Test for table creation in the database
3. Test the table existence in PostgreSQL database
4. Test if the consumer is able to subscribe and store the data to PostgreSQL database
5. Test if the data is stored in the database
6. Run all tests!
7. Exit the Test suite!
```
Test 1:
- This test is used to validate `producer fucntion` from `producer.py` by creating a `test_topic` and send one fake generated movie ticket to the Kafka cluster.

Test 2:
- This test is used to validate `table creation` from `db_setup.py` by creating a new `test_table` in PostgreSQL database.

Test 3:
- This test is used to validate table existence in the database.

Test 4:
- This test is used to validate `consumer function` from `consumer.py` by subscribing to `test_topic` and store the test messages to the `test_table` in the PostgreSQL database.

Test 5:
- This test is used to validate if the data stored by the consumer exists or not.

Test 6:
- Running all the tests in the sequence. This test the entire pipeline functionality.

## Future improvements needed
- Validating if the database contains the same `ticket_id` before trying to store the ticket message.
- For the movie ticketing applciation, it is better to have few more tables like `seating`and `transaction` to make the ticketing system foolproof.
- Adding a logging file that keeps the history of publish and subscribe metrics.
- Allow users to choose the database or schema.
- Improve the test suit - adding tests for validating messages in the `kafka cluster`.

## References
- Kafka tutorial : [https://timber.io/blog/hello-world-in-kafka-using-python/#1-simplify-the-backend-architecture](https://timber.io/blog/hello-world-in-kafka-using-python/#1-simplify-the-backend-architecture)
- Using Aiven Kafka service : [https://aiven.io/blog/create-your-own-data-stream-for-kafka-with-python-and-faker](https://aiven.io/blog/create-your-own-data-stream-for-kafka-with-python-and-faker)
- Using Aiven PostgreSQL service [https://help.aiven.io/en/articles/489573-getting-started-with-aiven-for-postgresql](https://help.aiven.io/en/articles/489573-getting-started-with-aiven-for-postgresql)


