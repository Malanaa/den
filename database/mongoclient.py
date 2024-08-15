import pymongo
import certifi
from datetime import date
import os
from dotenv import load_dotenv


load_dotenv()
mongo_connection_string = os.environ.get("CUSTOMCONNSTR_MONGO_CONNECTION_STRING")
print(mongo_connection_string)

if not mongo_connection_string or not mongo_connection_string.startswith(
    ("mongodb://", "mongodb+srv://")
):
    raise ValueError("MONGO_CONNECTION_STRING is not set correctly in the environment.")

# Creating the MongoDB Client
client = pymongo.MongoClient(
    mongo_connection_string,
    tlsCAFile=certifi.where(),
)
