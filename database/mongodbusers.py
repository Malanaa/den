import pymongo
import certifi
from datetime import date
import os
from dotenv import load_dotenv


load_dotenv()

mongo_connection_string = os.getenv("MONGO_CONNECTION_STRING")

# MongoDB Client
client = pymongo.MongoClient(
    mongo_connection_string,
    tlsCAFile=certifi.where(),
)


# Creating the Users Collection
udb = client["Users"]
users = udb["users"]

# Init the Indexes by running the script
if __name__ == "__main__":
    users.create_index("email", unique=True)
    users.create_index("password")


"""

Example User Json

user = {

                        "email" : "email",
                        "password_hash" : "hashed_password",
                    }

"""
