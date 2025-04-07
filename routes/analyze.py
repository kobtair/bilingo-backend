from flask import Blueprint, request, jsonify
import os
import tempfile
from difflib import SequenceMatcher
from Levenshtein import distance as levenshtein_distance
from ml import transcribe_audio, text_to_pinyin, simplify_pinyin

STORAGE_PATH = r"D:\bilingo\bilingo-backend"


analyze_routes = Blueprint("analyze", __name__)

@analyze_routes.route('/analyze', methods=['POST'])
def analyze_audio():
    # Get base_audio_id from request form
    base_audio_id = request.form.get('base_audio_id')
    if not base_audio_id:
        return jsonify({"error": "Missing base_audio_id"}), 400
    if 'audio_file' not in request.files:
        return jsonify({"error": "Missing audio_file in request"}), 400

    base_audio_path = os.path.join(STORAGE_PATH, f"{base_audio_id}.wav")
    if not os.path.isfile(base_audio_path):
        return jsonify({"error": "Base audio file not found"}), 404

    # Save uploaded file temporarily
    audio_file = request.files['audio_file']
    tmp_dir = tempfile.gettempdir()
    upload_path = os.path.join(tmp_dir, audio_file.filename)
    try:
        audio_file.save(upload_path)
    except Exception as e:
        return jsonify({"error": f"Failed to save file to temporary location: {str(e)}"}), 500

    try:
        # Process base audio file
        transcription1 = transcribe_audio(base_audio_path)
        pinyin_phonetics1 = text_to_phonetics(transcription1)
        plain_phonetics1 = text_to_plain_phonetics(transcription1)

        # Process uploaded audio file
        transcription2 = transcribe_audio(upload_path)
        pinyin_phonetics2 = text_to_phonetics(transcription2)
        plain_phonetics2 = text_to_plain_phonetics(transcription2)

        # Compare phonetics using SequenceMatcher on plain phonetics
        ratio = SequenceMatcher(None, plain_phonetics1, plain_phonetics2).ratio()
    finally:
        if os.path.exists(upload_path):
            os.remove(upload_path)

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
             "similarity_ratio": ratio
         }
    })

# Register additional routes or blueprint actions as needed
