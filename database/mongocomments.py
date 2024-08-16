from .mongoclient import client

# Creating the Users Collection
cdb = client["Comments"]
comments = cdb["comments"]

# Init the Indexes by running the script
if __name__ == "__main__":
    comments.create_index("user")
    comments.create_index("blog")
    comments.create_index("comment")
    comments.create_index("time")


"""

Example Comments Json

comment = {

                        "user" : "xyz@domain.com",
                        "blog" : "blog_id",
                        "comment" : "This sucks",
                        "time": str(date.today()),
                    }

"""
