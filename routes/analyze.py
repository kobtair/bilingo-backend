from flask import Blueprint, request, jsonify
import os
import tempfile
from ml2_api import transcribe_audio_api, text_to_phonetics, text_to_plain_phonetics, compare_phonetics
from config import user_collection, audio_collection
from bson.objectid import ObjectId

analyze_routes = Blueprint("analyze", __name__)

@analyze_routes.route('/analyze', methods=['POST'])
def analyze_audio():
    # Get audio_id from request form
    audio_id = request.form.get('audio_id')
    if not audio_id:
        return jsonify({"error": "Missing audio_id"}), 400

    # Retrieve base_audio_url from the database
    audio_doc = audio_collection.find_one({"_id": ObjectId(audio_id)})
    if not audio_doc or 'fileUrl' not in audio_doc:
        return jsonify({"error": "Invalid audio_id or URL not found"}), 400

    base_audio_url = audio_doc['fileUrl']

    if 'audio' not in request.files:
        return jsonify({"error": "Missing audio_file in request"}), 400

    # Save uploaded file temporarily
    audio_file = request.files['audio']
    tmp_dir = tempfile.gettempdir()
    upload_path = os.path.join(tmp_dir, audio_file.filename)
    try:
        audio_file.save(upload_path)
    except Exception as e:
        return jsonify({"error": f"Failed to save file: {str(e)}"}), 500

    try:
        # Process base audio from URL
        transcription1 = transcribe_audio_api(base_audio_url)
        pinyin_phonetics1 = text_to_phonetics(transcription1)
        plain_phonetics1 = text_to_plain_phonetics(transcription1)

        # Process uploaded audio file
        transcription2 = transcribe_audio_api(upload_path)
        pinyin_phonetics2 = text_to_phonetics(transcription2)
        plain_phonetics2 = text_to_plain_phonetics(transcription2)

        # Compare plain phonetics
        comparison_results = compare_phonetics(plain_phonetics1, plain_phonetics2)
    finally:
        if os.path.exists(upload_path):
            os.remove(upload_path)

    # Update user points if user_id is provided
    user_id = request.form.get('user_id')
    points_gained = 0
    if user_id:
        points = int(comparison_results["similarity_ratio"] * 100)
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
         "comparison": comparison_results,
         "points": points_gained
    })
