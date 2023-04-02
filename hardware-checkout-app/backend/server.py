from flask import Flask, render_template, request, jsonify, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util
from flask_cors import CORS
import cipher

app = Flask(__name__)

client = MongoClient('mongodb+srv://EE461LSp23:team@cluster0.kpubrms.mongodb.net/test')
db = client['users']
users_collection = db['users']

db1 = client['Projects']
project_collection = db1['test']

db2 = client['HardwareSets']

CORS(app)

@app.route('/signup', methods=['POST'])
def signup():
    userId = request.json['userId']
    password = request.json['password']

    if users_collection.find_one({'userID': userId}):
        return jsonify({'error': 'User already exists'})
    
    filter = {"name": "HWSet1"}
    new_values = {f"userHardware.{userId}": 0}
    db2['HWSet1'].update_one(filter, { "$set": new_values})

    filter = {"name": "HWSet2"}
    new_values = {f"userHardware.{userId}": 0}
    db2['HWSet2'].update_one(filter, { "$set": new_values})

    encrypt = cipher.encrypt(password, 4, -1)
    encryptId = cipher.encrypt(userId, 4, -1)

    post = {
        "userID": encryptId,
        "password": encrypt,
        "projects": []
    }
    result = users_collection.insert_one(post)
    if result.inserted_id:
        return jsonify({'success': True})
    else:
        return{'success': False}

@app.route('/login', methods=['POST'])
def login():
    userId = request.json['userId']
    password = request.json['password']

    # find user in the database
    encryptId = cipher.encrypt(userId, 4, -1)
    user = users_collection.find_one({'userID': encryptId})

    # check if user exists
    if not user:
        return jsonify({'error': 'User not found'})

    decrypt = cipher.decrypt(user['password'], 4, -1)
    # check if password is correct
    if not password == decrypt:
        return jsonify({'error': 'Incorrect password'})

    response = {'success': True}
    return jsonify(response)

@app.route('/home', methods=['POST'])
def home():
    userId = request.json['userId']
    idencrypt = cipher.encrypt(userId, 4, -1)
    document = users_collection.find_one({'userID': idencrypt})
    array = document['projects']

    documents = project_collection.find({'id': {'$in': array}})

    json_data = json_util.dumps(documents)
   
    return jsonify(json_data)


@app.route('/join', methods=['POST'])
def join():
    projectId = request.json['projectId']
    userId = request.json['userId']
    idencrypt = cipher.encrypt(userId, 4, -1)
    project = project_collection.find_one({'id': projectId})
    if not project:
        return jsonify({'error': 'Project not found'})
    
    member = project['Users']
    if userId in member:
        return jsonify({'error': 'Already joined the project'})

    project_collection.update_one(
        {'id': projectId},
        {'$push': {'Users': userId}}
    )

    users_collection.update_one(
        {'userID': idencrypt},
        {'$push': {'projects': projectId}}
    )

    return jsonify({'message': projectId, 'userId': userId, 'success': True})


@app.route('/leave', methods=['POST'])
def leave():
    projectId = request.json['projectId']
    userId = request.json['userId']
    idencrypt = cipher.encrypt(userId, 4, -1)
    project = project_collection.find_one({'id': projectId})
    if not project:
        return jsonify({'error': 'Project not found'})
    
    project_collection.update_one(
        {'id': projectId},
        {'$pull': {'Users': userId}}
    )

    users_collection.update_one(
        {'userID': idencrypt},
        {'$pull': {'projects': projectId}}
    )

    return jsonify({'message': projectId, 'userId': userId})
    # return jsonify({'message': projectId})
      
@app.route('/gethardware', methods=['POST'])
def get_hardware():
    collections = db2.list_collection_names()
    return jsonify(collections)

@app.route('/getnumhardware', methods=['POST'])
def get_num_hardware():
    name = request.json['name']
    document = db2[name].find_one({'name': name})
    cap = document['capacity']
    avail = document['availability']
    array = [cap, avail]
    return jsonify(array)

@app.route('/checkouthardware', methods=['POST'])
def checkout():
    name = request.json['name']
    number = request.json['change']
    id = request.json['userId']
    integer = int(number)
    document = db2[name].find_one({'name': name})
    avail = document['availability']
    if integer > avail:
        return jsonify({'status': False})
    query = {'name': name}
    new_avail = avail - integer
    new_values = {'$set': {'availability': new_avail}}
    db2[name].update_one(query, new_values)

    result = db2[name].find_one(query)
    currentValue = result["userHardware"][id]
    cvint = int(currentValue)
    cvint = cvint + integer

    new_values = {f"userHardware.{id}": cvint}
    db2[name].update_one(query, { "$set": new_values})

    return jsonify({'status': True, 'number': new_avail})

@app.route('/checkin', methods=['POST'])
def checkin():
    name = request.json['name']
    number = request.json['change']
    id = request.json['userId']
   
    integer = int(number)
    document = db2[name].find_one({'name': name})
    avail = document['availability']
    cap = document['capacity']

    query = {'name': name}
    
    result = db2[name].find_one(query)
    currentValue = result["userHardware"][id]
    cvint = int(currentValue)
    if integer > cvint:
        return jsonify({'status': False, 'message': 'Error: Cannot check in more than user has checked out'})

    cvint = cvint - integer

    new_values = {f"userHardware.{id}": cvint}
    db2[name].update_one(query, { "$set": new_values})

    if integer + avail > cap:
        return jsonify({'status': False, 'message': 'Check-in request exceeds the capacity'})
    new_avail = avail + integer
    new_values = {'$set': {'availability': new_avail}}
    db2[name].update_one(query, new_values)


    return jsonify({'status': True, 'number': new_avail})

@app.route('/create', methods=['POST'])
def create():
    id = request.json['id']
    name = request.json['name']
    description = request.json['description']
    if project_collection.find_one({'id': id}):
        return jsonify({'status': False,'message': 'Project ID already exists'})
    
    post = {
        "id": id,
        "name": name,
        "description": description,
        "Users": [],
        "isMember": "false"
    }
    result = project_collection.insert_one(post)
    if result.inserted_id:
        return jsonify({'success': True})
    else:
        return{'success': False}


# Running app
if __name__ == '__main__':
    app.run(debug=True)