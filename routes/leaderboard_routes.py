from flask import Blueprint, jsonify
from config import user_collection

leaderboard_routes = Blueprint('leaderboard_routes', __name__)

@leaderboard_routes.route('/get-leaderboard', methods=['GET'])
def get_leaderboard():
    leaderboard = list(user_collection.find().sort("points", -1))
    return jsonify(leaderboard)
