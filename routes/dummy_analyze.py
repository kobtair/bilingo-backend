from flask import Blueprint, jsonify, request
import time
import random
from config import user_collection
from bson.objectid import ObjectId

dummy_analyze_routes = Blueprint("dummy_analyze", __name__)

def update_user_points(user_id, similarity_ratio):
    points = int(similarity_ratio * 100)
    result = user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$inc": {"points": points}}
    )
    if result.modified_count:
        print(f"Updated user {user_id}'s points by {points}")
        return points
    else:
        print(f"User {user_id} not found or points not updated")
        return 0

@dummy_analyze_routes.route('/analyze/dummy', methods=['POST'])
def dummy_analyze_audio():
    # Determine request content type and extract data accordingly
    if request.is_json:
        data = request.get_json()
    elif request.form:
        data = request.form
    else:
        return jsonify({"error": "Content-Type must be application/json or form-data"}), 415

    # Simulate processing delay
    time.sleep(5)
    
    # Extract user_id from the data
    user_id = data.get("user_id")
    
    # Define multiple realistic outputs with Chinese audio content
    outputs = [
        {
            "base_audio": {"transcription": "晚上好,今天過得怎麼樣?", "pinyin": "wan3 shang4   hao3  ,  jin1 tian1   guo4 de2   zen3 me yang4  ?", "plain": "晚上好,今天過得怎麼樣?"},
            "uploaded_audio": {"transcription": " 晚上好,今天过得人美样。", "pinyin": "wan3 shang4   hao3  ,  jin1 tian1   guo4 de2   ren2 mei3 yang4  。", "plain": "晚上好,今天过得人美样。"},
            "comparison": {"similarity_ratio": 0.95}
        },
        # {
        #     "base_audio": {"transcription": "示例语音", "pinyin": "shì lì yǔ yīn", "plain": "文本示例"},
        #     "uploaded_audio": {"transcription": "示例语音改", "pinyin": "shì lì yǔ yīn gǎi", "plain": "文本替换"},
        #     "comparison": {"similarity_ratio": 0.85}
        # },
        # {
        #     "base_audio": {"transcription": "测试段落", "pinyin": "cè shì duàn luò", "plain": "纯文本"},
        #     "uploaded_audio": {"transcription": "测试段落修正", "pinyin": "cè shì duàn luò xiū zhèng", "plain": "纯文本修正"},
        #     "comparison": {"similarity_ratio": 0.75}
        # }
    ]
    
    # Randomly select one output to return
    response = random.choice(outputs)
    
    # Update user points using actual DB update and receive points added
    points_gained = update_user_points(user_id, response["comparison"]["similarity_ratio"])
    
    # Add the points to the response
    response["points"] = points_gained
    
    return jsonify(response)
