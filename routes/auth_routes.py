from flask import Blueprint, request
from config import user_collection
from utils import hash_password, check_password

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        return 'No data received', 400
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return 'Email or Password is missing', 400
    current_user = user_collection.find_one({'email': email})
    if current_user and check_password(password, current_user["password"]):
        return 'Login Success'
    else:
        return 'Login Failed', 401

@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data:
        return 'No data received', 400
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    if not email or not password:
        return 'Email or Password is missing', 400
    if '@' not in email:
        return 'Invalid Email', 400
    if len(password) < 6:
        return 'Password is too short', 400
    hashed_password = hash_password(password)
    user_collection.insert_one({
        'name': name,
        'email': email,
        'password': hashed_password,
        'points': 0
    })
    return 'User Registered Successfully'
