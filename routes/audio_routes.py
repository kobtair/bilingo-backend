from flask import Blueprint, request, jsonify
from datetime import date
from config import audio_collection
from bson import ObjectId

audio_routes = Blueprint('audio_routes', __name__)

@audio_routes.route('/audio', methods=['GET'])
def get_all_audio():
    """
    Get all audio files.
    """
    audio_files = list(audio_collection.find())
    for audio in audio_files:
        audio['_id'] = str(audio['_id'])  # Convert ObjectId to string
    return jsonify(audio_files), 200

@audio_routes.route('/audio/<audio_id>', methods=['GET'])
def get_audio_by_id(audio_id):
    """
    Get an audio file by its ID.
    """
    audio = audio_collection.find_one({"_id": ObjectId(audio_id)})
    if not audio:
        return {"error": "Audio file not found"}, 404
    audio['_id'] = str(audio['_id'])  # Convert ObjectId to string
    return jsonify(audio), 200

@audio_routes.route('/audio', methods=['POST'])
def upload_audio():
    """
    Upload a new audio file.
    """
    data = {
        "id": request.form.get('id'),
        "title": request.form.get('title'),
        "language": request.form.get('language'),
        "dialect": request.form.get('dialect'),
        "phraseSaid": request.form.get('phraseSaid'),
        "fileName": request.form.get('fileName'),
        "fileUrl": request.form.get('fileUrl'),
        "duration": request.form.get('duration'),
        "uploadDate": date.today().strftime("%Y-%m-%d"),
    }
    audio_id = audio_collection.insert_one(data).inserted_id
    return {"message": "Audio file uploaded successfully", "audio_id": str(audio_id)}, 201

@audio_routes.route('/audio/<audio_id>', methods=['DELETE'])
def delete_audio(audio_id):
    """
    Delete an audio file by its ID.
    """
    result = audio_collection.delete_one({"id": audio_id})
    if result.deleted_count == 0:
        return {"error": "Audio file not found"}, 404
    return {"message": "Audio file deleted successfully"}, 200

