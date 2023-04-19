import pytest_check as check
import requests
from .. import cipher
from pymongo import MongoClient

client = MongoClient('mongodb+srv://EE461LSp23:team@cluster0.kpubrms.mongodb.net/test')
db = client['users']
users_collection = db['users']
db1 = client['Projects']
project_collection = db1['test']
db2 = client['HardwareSets']

def test_user_signup():
    userId = 'asamant'
    password = 'Temp123'

    requests.post('http://localhost:5000/signup', json={
        'userId': userId,
        'password': password
    })

    encrypt = cipher.encrypt(password, 4, -1)
    encryptId = cipher.encrypt(userId, 4, -1)

    user = users_collection.find_one({'userID': encryptId})
    check.is_not_none(user, "User not added to Database")
    check.equal(encrypt, user['password'], 'User name or Password does not match')

def test_user_signin():
    userId = 'asamant'
    password = 'Temp123'
    encrypt = cipher.encrypt(password, 4, -1)
    encryptId = cipher.encrypt(userId, 4, -1)

    response = requests.post('http://localhost:5000/login', json={
        'userId': userId,
        'password': password
    })
    check.equal({'success': True}, response.json(), "Incorrect Login information")

def test_create_project():
    projectid = 'P123'
    name = 'Project 123'
    description = 'test create project'
    result = requests.post('http://localhost:5000/create', json={
      'id': projectid,
      'name': name,
      'description': description
    })

    project = project_collection.find_one({'id': projectid})
    check.is_not_none(project, "Project ID not found in Database")
    dbname = project['name']
    check.equal(name, dbname, "Project name does not match")
    dbdescription = project['description']
    check.equal(description, dbdescription, "Project description does not match")

def test_join_project():
    projectid = 'P123'
    userId = 'asamant'
    result = requests.post('http://localhost:5000/join', json={
        'projectId': projectid,
        'userId': userId
    })

    project = project_collection.find_one({'id': projectid})
    users = project['Users']
    check.is_in(userId, users, "User did not join Project correctly")
    encryptId = cipher.encrypt(userId, 4, -1)
    user = users_collection.find_one({'userID': encryptId})
    check.is_in(projectid, user['projects'], 'User did not join Project correctly')

def test_leave_project():
    projectid = 'P123'
    userId = 'asamant'
    result = requests.post('http://localhost:5000/leave', json={
        'projectId': projectid,
        'userId': userId
    })

    check.not_equal({'error': 'Project not found'}, result.json(), "Project not found")

    project = project_collection.find_one({'id': projectid})
    users = project['Users']
    check.is_not_in(userId, users, "User did not leave Project correctly")
    encryptId = cipher.encrypt(userId, 4, -1)
    user = users_collection.find_one({'userID': encryptId})
    check.is_not_in(projectid, user['projects'], 'User did not join Project correctly')

def test_checkin():
    change = 10
    name = 'HWSet1'
    userId = 'abhi'
    HWSet = db2[name].find_one({'name': name})
    initialValue = int(HWSet['userHardware'][userId])
    initialAvailabilty = HWSet['availability']
    result = requests.post('http://localhost:5000/checkin', json={
        'change': change,
        'name': name,
        'userId': userId
    })

    check.is_true(result.json()['status'], "Trying to checkin more than is checked out")
    HWSet = db2[name].find_one({'name': name})
    currentValue = int(HWSet['userHardware'][userId])
    check.equal(initialValue-change, currentValue, "Number of tools checked in does not match expected outcome")
    check.equal(HWSet['availability'], initialAvailabilty+change, "HWSet availability not updated correctly")

def test_checkout():
    change = 10
    name = 'HWSet1'
    userId = 'abhi'
    HWSet = db2[name].find_one({'name': name})
    initialValue = int(HWSet['userHardware'][userId])
    initialAvailabilty = HWSet['availability']
    result = requests.post('http://localhost:5000/checkouthardware', json={
        'change': change,
        'name': name,
        'userId': userId
    })

    check.is_true(result.json()['status'], "Availability is less than desired checkout")
    HWSet = db2[name].find_one({'name': name})
    currentValue = int(HWSet['userHardware'][userId])
    check.equal(initialValue+change, currentValue, "Number of tools checked out does not match expected outcome")
    check.equal(HWSet['availability'], initialAvailabilty-change, "HWSet availability not updated correctly")

