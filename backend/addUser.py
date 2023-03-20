import pymongo
from pymongo.errors import ConnectionFailure
from website.src import cipher
def addNewUser(username, userid, password):
    try:
        client = pymongo.MongoClient(
            "mongodb+srv://EE461LSp23:team@cluster0.kpubrms.mongodb.net/?retryWrites=true&w=majority"
        )
        client.server_info()  # will throw an exception
    except ConnectionFailure:
        print("Server not available")

    db = client.Users
    myCollection = db[username]
    me = {
        "userid": userid,
        "password": cipher.encrypt(password, 3, 1)
    }
    myCollection.insert_one(me)
    client.close()
    return

def login(username, userid, password):
    try:
        client = pymongo.MongoClient(
            "mongodb+srv://EE461LSp23:team@cluster0.kpubrms.mongodb.net/?retryWrites=true&w=majority"
        )
        client.server_info()  # will throw an exception
    except ConnectionFailure:
        print("Server not available")
