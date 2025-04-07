from flask import Blueprint, request, jsonify
import math

progress_routes = Blueprint("progress_routes", __name__)

# In-memory progress storage (for demo purposes)
user_progress = {
    "test@example.com": {
        "overallProgress": 33,
        "completedLessons": [1],
        "totalLessons": 3,
        "score": 90,
        "rank": 2,
    },
}

@progress_routes.route('/progress', methods=['GET'])
def get_progress():
    email = request.args.get("email")
    if not email:
        return jsonify({"error": "Email is required"}), 400
    if email not in user_progress:
        # Auto-create default progress if not found
        user_progress[email] = {
            "overallProgress": 0,
            "completedLessons": [],
            "totalLessons": 3,
            "score": 0,
            "rank": 0,
        }
    return jsonify(user_progress[email]), 200

@progress_routes.route('/get-leaderboard', methods=['GET'])
def get_leaderboard():
    # Sort users by score descending
    leaderboard = sorted(
        [{"email": email, **data} for email, data in user_progress.items()],
        key=lambda x: x["score"],
        reverse=True
    )
    return jsonify(leaderboard), 200

@progress_routes.route('/chapter-complete', methods=['POST'])
def chapter_complete():
    data = request.get_json()
    email = data.get("email")
    lesson_id = data.get("lessonId")
    if not email or lesson_id is None:
        return jsonify({"error": "Email and lessonId are required"}), 400

    if email not in user_progress:
        user_progress[email] = {
            "overallProgress": 0,
            "completedLessons": [],
            "totalLessons": 3,
            "score": 0,
            "rank": 0,
        }
    
    progress = user_progress[email]
    if lesson_id not in progress["completedLessons"]:
        progress["completedLessons"].append(lesson_id)
        progress["overallProgress"] = round(
            (len(progress["completedLessons"]) / progress["totalLessons"]) * 100
        )
        progress["score"] += 10
        # Optionally update rank; here rank remains unchanged for simplicity
    
    return jsonify({"success": True}), 200
