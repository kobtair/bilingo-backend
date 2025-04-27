from flask import Blueprint, request, jsonify
from config import user_collection

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/update-points', methods=['POST'])
def update_points():
    data = request.json
    if not data:
        return 'No data received', 400
    email = data.get('email')
    points = data.get('points')
    if not email or not points:
        return 'Email or Points is missing', 400
    current_user = user_collection.find_one({'email': email})
    user_collection.update_one({'email': email}, {'$set': {'points': current_user['points'] + points}})
    return 'Points Updated Successfully'

@user_routes.route('/users', methods=['GET'])
def get_users():
    users = list(user_collection.find({}))
    for user in users:
        for key in list(user.keys()):
            if isinstance(user[key], bytes):
                user[key] = user[key].decode('utf-8')
                user['_id'] = str(user['_id'])
    return jsonify(users)