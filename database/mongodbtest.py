from mongodbusers import users
from mongodbposts import posts
from datetime import date

# for post in posts.find():
#     print(post["title"])
#     print(post["description"])
#     print(post["author"])
#     print(post["time"])
#     print(post["body"])
# Testing if posts find works

post = {
    "title": "How I overcame the fear of food",
    "description": "Hello this is a Sameple Description",
    "author": "Malanaa",
    "time": str(date.today()),
    "body": "This is a sample markdown format **Empasize this monkey",
}


# Just some db testing
