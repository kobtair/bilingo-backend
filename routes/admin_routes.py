from flask import Blueprint, request

admin_routes = Blueprint('admin_routes', __name__)

@admin_routes.route('/admin-login', methods=['POST'])
def admin_login():
    data = request.json
    if not data:
        return 'No data received', 400
    email = data.get('email')
    password = data.get('password')
    if email == "admin" and password == "admin":
        return 'Admin Login Success'
    else:
        return 'Admin Login Failed', 401
