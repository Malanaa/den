import pymongo
import certifi
from datetime import date
import os
from dotenv import load_dotenv
from .mongoclient import client

# load_dotenv()
# mongo_connection_string = os.getenv("MONGO_CONNECTION_STRING")


# if not mongo_connection_string or not mongo_connection_string.startswith(
#     ("mongodb://", "mongodb+srv://")
# ):
#     raise ValueError("MONGO_CONNECTION_STRING is not set correctly in the environment.")

# # Creating the MongoDB Client
# client = pymongo.MongoClient(
#     mongo_connection_string,
#     tlsCAFile=certifi.where(),
# )


# Creating the post collection
pdb = client["Posts"]
posts = pdb["posts"]


# Running the script to init the indexes
if __name__ == "__main__":
    posts.create_index("title")
    posts.create_index("description")
    posts.create_index("author")
    posts.create_index("time")
    posts.create_index("body")


"""

Example Posts Json

post = {

                        "title" : "It's really a mess",
                        "description": "Hello this is a Sameple Description",
                        "author" : "Malanaa",
                        "time" : str(date.today()),
                        "body": "This is a sample markdown format **Empasize this monkey",
                    }


"""
