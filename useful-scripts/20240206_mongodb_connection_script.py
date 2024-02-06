"""
Description: This is a script to connect to a MongoDB Atlas cluster. I may need to use it later!

Date: Tue. 2/6/24 @ 2:15 PM EST
"""

# Importing the required library.
from pymongo import MongoClient

# Setting the MongoDB Atlas cluster url. Make sure that the URL is replaced if you create a new cluster!
# - user: 'myAtlasDBUser'
# - password: '*'
# - Atlas cluster name: 'myatlasclusteredu'
url = "mongodb+srv://myAtlasDBUser:*@myatlasclusteredu.uh8jjxt.mongodb.net/?retryWrites=true&w=majority"

# Creating the client.
client = MongoClient(url)

# Testing the connection to the cluster.
try:
    client.admin.command('ismaster')
    print("\nConnection to MongoDB Atlas successful!\n")
except Exception as e:
    print("\nUnable to connect to MongoDB Atlas.\n")
    print(e)

# Printing the list of databases.
# print(client.list_database_names())

# Access a specific database.
db = client.sample_analytics

# Perform an operation on the database, for example list all collections in 
# the database.
print(db.list_collection_names())
print()