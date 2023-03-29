from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import MongoClient
from flask_cors import CORS

client = MongoClient('mongodb+srv://drewconyers:hookem@cluster0.kyjwozy.mongodb.net/test')

db = client['Projects']
projects_collection = db['Project1']

projects = projects_collection.find()
result = []
for project in projects:
    project['_id'] = str(project['_id'])
    result.append(project)


print(result)