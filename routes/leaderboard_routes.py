from flask import Blueprint, jsonify
from config import user_collection

leaderboard_routes = Blueprint('leaderboard_routes', __name__)

@leaderboard_routes.route('/get-leaderboard', methods=['GET'])
def get_leaderboard():
    leaderboard = list(user_collection.find().sort("points", -1))
    ranked_leaderboard = []
    for rank, user in enumerate(leaderboard, start=1):
        user['_id'] = str(user['_id'])
        for key, value in user.items():
            if isinstance(value, bytes):  # Check if the value is of type bytes
                user[key] = value.decode('utf-8')  # Decode bytes to string
        ranked_leaderboard.append({
            "rank": rank,
            "name": user.get("name"),
            "points": user.get("points")
        })
    return jsonify(ranked_leaderboard)
