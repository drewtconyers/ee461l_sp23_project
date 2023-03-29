from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={"/api/*": {"origins": "*"}})

client = MongoClient('mongodb+srv://drewconyers:hookem@cluster0.kyjwozy.mongodb.net/test')

db = client['Projects']
projects_collection = db['Project1']


@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = projects_collection.find()
    result = []
    for project in projects:
        project['_id'] = str(project['_id'])
        result.append(project)
    return jsonify(result)

@app.route('/api/projects/<project_id>/check-in', methods=['POST'])
def check_in_hardware(project_id):
    qty = request.json['qty']
    project = projects_collection.find_one({"_id": ObjectId(project_id)})

    # Calculate available hardware for check-out
    available_hardware = project['hardware_qty']
    actual_checkout_qty = min(available_hardware, qty)

    # Update the project's hardware quantity in the database
    projects_collection.update_one(
        {"_id": ObjectId(project_id)},
        {"$inc": {"hardware_qty": available_hardware + qty}}
    )

    if actual_checkout_qty < qty:
        return jsonify({"error": "Not enough hardware available. Only checked out {} items.".format(actual_checkout_qty)}), 400

    return jsonify({"projectId": project_id, "qty": actual_checkout_qty})

@app.route('/api/projects/<project_id>/check-out', methods=['POST'])
def check_out_hardware(project_id):
    qty = request.json['qty']
    project = projects_collection.find_one({"_id": ObjectId(project_id)})

    # Calculate available hardware for check-out
    available_hardware = project['hardware_qty']
    actual_checkout_qty = min(available_hardware, qty)

    # Update the project's hardware quantity in the database
    projects_collection.update_one(
        {"_id": ObjectId(project_id)},
        {"$inc": {"hardware_qty": (available_hardware - qty)}}
    )

    if actual_checkout_qty < qty:
        return jsonify({"error": "Not enough hardware available. Only checked out {} items.".format(actual_checkout_qty)}), 400

    return jsonify({"projectId": project_id, "qty": actual_checkout_qty})


@app.route('/api/projects/<project_id>/join', methods=['POST'])
def join_project(project_id):
    username = request.json['username']
    projects_collection.update_one(
        {"_id": ObjectId(project_id)},
        {"$addToSet": {"users": username}}
    )
    return jsonify({"message": f"Joined {project_id}"})

@app.route('/projects/<project_id>/leave', methods=['POST'])
def leave_project(project_id):
    username = request.json['username']
    projects_collection.update_one(
        {"_id": ObjectId(project_id)},
        {"$pull": {"users": username}}
    )
    return jsonify({"message": f"Left {project_id}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
