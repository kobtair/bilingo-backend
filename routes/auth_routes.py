from flask import Blueprint, request, jsonify, make_response
from config import user_collection
from utils import hash_password, check_password, generate_jwt

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
        token_payload = {
            'user_id': str(current_user['_id']),
            'email': current_user['email'],
            'is_admin': current_user.get('is_admin', False)
        }
        token = generate_jwt(token_payload)
        response = make_response(jsonify({'message': 'Login Success'}))
        response.set_cookie('user_token', token, httponly=True)
        response.set_cookie('is_admin', str(current_user.get('is_admin', False)), httponly=True)
        return response
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
