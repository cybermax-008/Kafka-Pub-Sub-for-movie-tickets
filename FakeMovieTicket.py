import random
from faker import Faker
"""
This script generates random messages of movie ticket orders that is to be published to Kafka cluster
(using producer) and subscribed by the consumer and finally stored in database.
"""
class TicketGen():
    """
    Fake ticket data generation,
    - theater name
    - movie name
    - user name, phone and email
    - seats
    """
    def __init__(self,ticket_id=1): # NEEDS IMPROVEMENT: ticket_id by default 1, instead we can get the last id in database and keep the next number as id.
        self.fake = Faker()
        self.ticket_id = ticket_id

    def theater(self):
        # assume there are 5 theaters
        types = ["A","B","C","D","E"]
        theater = "{} {}".format("Theater",types[random.randint(0,len(types)-1)])
        return theater
    
    def userInfo(self):
        # create fake user details
        domain = ["gmail.com", "yahoo.com", "hotmail.com","icloud.com"]
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        full_name = "{} {}".format(first_name,last_name)
        email = "{}.{}@{}".format(first_name,last_name,domain[random.randint(0,len(domain)-1)])
        phone = self.fake.unique.phone_number()
        return [full_name,email,phone]

    def movieName(self):
        # assuming current movies in the city that are screened
        movies_screening = ["Avengers:The End Game",
                            "The Departed",
                            "The Forbidden Kingdom",
                            "October Sky",
                            "The Hobbit",
                            "The Dark Knight Rises",
                            "Justice League",
                            "Tenet",
                            "Shazam",
                            "The Maze Runner"
                            ]
        self.movie = movies_screening[random.randint(0,len(movies_screening)-1)]
        return self.movie

    def seats(self):
        # random seat name generation
        row = [chr(i) for i in range(65,65+26)]
        col = list(range(1,11))
        seat = "{}{}".format(row[random.randint(0,len(row)-1)],col[random.randint(0,len(col)-1)])
        return seat


