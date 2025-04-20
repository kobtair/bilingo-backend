from flask import Blueprint, request, jsonify
import os
import tempfile
from difflib import SequenceMatcher
from ml2_api import transcribe_audio, text_to_pinyin, simplify_pinyin
from config import user_collection, audio_collection
from bson.objectid import ObjectId
import requests

STORAGE_PATH = r"D:\bilingo\bilingo-backend"

analyze_routes = Blueprint("analyze", __name__)

@analyze_routes.route('/analyze', methods=['POST'])
def analyze_audio():
    # Get base_audio_id from request form
    base_audio_id = request.form.get('base_audio_id')
    if not base_audio_id:
        return jsonify({"error": "Missing base_audio_id"}), 400

    # New: Retrieve base audio fileUrl from audio_collection
    base_audio_record = audio_collection.find_one({"_id": ObjectId(base_audio_id)})
    if not base_audio_record:
        return jsonify({"error": "Base audio record not found"}), 404
    file_url = base_audio_record.get("fileUrl")
    if not file_url:
        return jsonify({"error": "File URL not found in base audio record"}), 404

    tmp_dir = tempfile.gettempdir()
    tmp_base_path = os.path.join(tmp_dir, f"{base_audio_id}_base.wav")
    try:
        response = requests.get(file_url)
        if response.status_code != 200:
            return jsonify({"error": "Failed to download base audio"}), 500
        with open(tmp_base_path, 'wb') as f:
            f.write(response.content)
    except Exception as e:
        return jsonify({"error": f"Error downloading base audio: {str(e)}"}), 500

    if 'audio_file' not in request.files:
        if os.path.exists(tmp_base_path):
            os.remove(tmp_base_path)
        return jsonify({"error": "Missing audio_file in request"}), 400

    # Save uploaded file temporarily
    audio_file = request.files['audio_file']
    upload_path = os.path.join(tmp_dir, audio_file.filename)
    try:
        audio_file.save(upload_path)
    except Exception as e:
        if os.path.exists(tmp_base_path):
            os.remove(tmp_base_path)
        return jsonify({"error": f"Failed to save file: {str(e)}"}), 500

    try:
        # Process downloaded base audio file
        transcription1 = transcribe_audio(tmp_base_path)
        pinyin_phonetics1 = text_to_pinyin(transcription1)
        plain_phonetics1 = simplify_pinyin(pinyin_phonetics1)

        # Process uploaded audio file
        transcription2 = transcribe_audio(upload_path)
        pinyin_phonetics2 = text_to_pinyin(transcription2)
        plain_phonetics2 = simplify_pinyin(pinyin_phonetics2)

        # Compare plain phonetics using SequenceMatcher
        similarity_ratio = SequenceMatcher(None, plain_phonetics1, plain_phonetics2).ratio()
    finally:
        if os.path.exists(upload_path):
            os.remove(upload_path)
        if os.path.exists(tmp_base_path):
            os.remove(tmp_base_path)

    # Update user points if user_id is provided
    user_id = request.form.get('user_id')
    points_gained = 0
    if user_id:
        points = int(similarity_ratio * 100)
        result = user_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$inc": {"points": points}}
        )
        if result.modified_count:
            points_gained = points

    return jsonify({
         "base_audio": {
             "transcription": transcription1,
             "pinyin": pinyin_phonetics1,
             "plain": plain_phonetics1
         },
         "uploaded_audio": {
             "transcription": transcription2,
             "pinyin": pinyin_phonetics2,
             "plain": plain_phonetics2
         },
         "comparison": {
             "similarity_ratio": similarity_ratio
         },
         "points": points_gained
    })
