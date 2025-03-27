from flask import Blueprint, request, jsonify, make_response
from utils import generate_jwt

admin_routes = Blueprint('admin_routes', __name__)

@admin_routes.route('/admin-login', methods=['POST'])
def admin_login():
    data = request.json
    if not data:
        return 'No data received', 400
    email = data.get('email')
    password = data.get('password')
    if email == "admin" and password == "admin":
        token_payload = {
            'email': email,
            'is_admin': True
        }
        token = generate_jwt(token_payload)
        response = make_response(jsonify({'message': 'Admin Login Success'}))
        response.set_cookie('admin_token', token, httponly=True)
        response.set_cookie('is_admin', 'True', httponly=True)
        return response
    else:
        return 'Admin Login Failed', 401
