from flask import Flask, render_template, request, jsonify, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)

client = MongoClient('mongodb+srv://EE461LSp23:team@cluster0.kpubrms.mongodb.net/test')
db = client['users']
users_collection = db['users']

CORS(app)

@app.route('/signup', methods=['POST'])
def signup():
    userId = request.json['userId']
    username = request.json['username']
    password = request.json['password']

    if users_collection.find_one({'username': username}):
        return jsonify({'error': 'User already exists'}), 400

    post = {
        "userID": userId,
        "username": username,
        "password": password
    }
    result = users_collection.insert_one(post)
    if result.inserted_id:
        return redirect('/home')
    else:
        return{'success': False}

@app.route('/login', methods=['POST'])
def login():
    userId = request.json['userId']
    username = request.json['username']
    password = request.json['password']

    # find user in the database
    user = users_collection.find_one({'username': username})

    # check if user exists
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # check if password is correct
    if not password == user['password']:
        return jsonify({'error': 'Incorrect password'}), 401

    return jsonify({'message': 'Logged in successfully'}), 200


      
# Running app
if __name__ == '__main__':
    app.run(debug=True)