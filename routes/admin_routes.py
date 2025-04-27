from flask import Blueprint, request, jsonify, make_response
from utils import generate_jwt
import os

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")

admin_routes = Blueprint('admin_routes', __name__)

@admin_routes.route('/admin-login', methods=['POST'])
def admin_login():
    data = request.json
    if not data:
        return 'No data received', 400
    email = data.get('email')
    password = data.get('password')
    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        token_payload = {
            'email': email,
            'is_admin': True
        }
        token = generate_jwt(token_payload)
        response = make_response(jsonify({'message': 'Admin Login Success'}))
        response.set_cookie('admin_token', token, httponly=True, secure=True)
        response.set_cookie('is_admin', 'True', httponly=True, secure=True)
        return response
    else:
        return 'Admin Login Failed', 401
