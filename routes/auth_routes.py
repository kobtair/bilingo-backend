from flask import Blueprint, request, jsonify, make_response
import datetime
from config import user_collection
from utils import hash_password, check_password, generate_jwt
import os  # Added for environment variable access

auth_routes = Blueprint('auth_routes', __name__)

def create_auth_response(user, message):
    """
    Helper function to generate JWT and set cookies.
    """
    token_payload = {
        'user_id': str(user['_id']),
        'email': user['email'],
        'is_admin': user.get('is_admin', False)
    }
    token = generate_jwt(token_payload)
    # Set secure cookies only in production
    is_secure = os.getenv("FLASK_ENV") == "production"
    response = make_response(jsonify({'user': user, 'message': message}))
    response.set_cookie('user_token', token, httponly=True, secure=is_secure)
    response.set_cookie('is_admin', str(user.get('is_admin', False)), httponly=True, secure=is_secure)
    return response

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
        current_user.pop('password')
        current_user['_id'] = str(current_user['_id'])
        # Ensure all fields are returned in the response
        current_user.setdefault('profileImage', '')
        current_user.setdefault('level', 'Beginner')
        current_user.setdefault('progress', 0)
        current_user.setdefault('lastActive', '')
        current_user.setdefault('joinDate', '')
        current_user.setdefault('status', 'Active')
        return create_auth_response(current_user, 'Login Success')
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
    primary_language = data.get('primaryLanguage')
    profile_image = data.get('profileImage', '')  # Optional field
    if not name:
        return 'Name is missing', 400
    if not primary_language:
        return 'Primary Language is missing', 400
    if not email or not password:
        return 'Email or Password is missing', 400
    if '@' not in email:
        return 'Invalid Email', 400
    if len(password) < 6:
        return 'Password is too short', 400
    hashed_password = hash_password(password)
    existingUser = user_collection.find_one({'email': email})
    if existingUser:
        return 'User already exists', 400
    try:
        user_collection.insert_one({
            'name': name,
            'email': email,
            'password': hashed_password,
            'language': primary_language,
            'profileImage': profile_image,
            'level': 'Beginner',  
            'progress': 0,  
            'lastActive': datetime.datetime.now().isoformat(),  
            'joinDate': datetime.datetime.now().isoformat(),
            'points': 0,  
            'status': 'Active'  
        })
    except Exception as e:
        return f"Database error: {str(e)}", 500
    current_user = user_collection.find_one({'email': email})
    current_user.pop('password')
    current_user['_id'] = str(current_user['_id'])
    return create_auth_response(current_user, 'User Registered Successfully')


