import pymongo
from pymongo.errors import ConnectionFailure
from flask import Flask

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

def queryHWSet1Availability(projectid):
    try:
        client = pymongo.MongoClient(
            "mongodb+srv://EE461LSp23:team@cluster0.kpubrms.mongodb.net/?retryWrites=true&w=majority"
        )
        client.server_info()  # will throw an exception
    except ConnectionFailure:
        print("Server not available")

    db = client["HardwareSets"]

    HWSet1 = db["HWSet1"]
    availability = 0
    for x in db.HWSet1.find({}):
        if x['ProjectID'] == projectid:
            availability = x['Availability']
    client.close()
    return availability


def queryHWSet2Availability(projectid):
    try:
        client = pymongo.MongoClient(
            "mongodb+srv://EE461LSp23:team@cluster0.kpubrms.mongodb.net/?retryWrites=true&w=majority"
        )
        client.server_info()  # will throw an exception
    except ConnectionFailure:
        print("Server not available")

    db = client["HardwareSets"]

    HWSet2 = db["HWSet2"]

    availability = 0
    for x in db.HWSet2.find({}):
        if x['ProjectID'] == projectid:
            availability = x['Availability']
    client.close()
    return availability