from flask import Blueprint, request, jsonify
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
    if 'file' not in request.files:
        return {"error": "No file provided"}, 400
    file = request.files['file']
    audio_id = audio_collection.insert_one({"filename": file.filename}).inserted_id
    # Save file to disk or cloud storage here
    return {"message": "Audio file uploaded successfully", "audio_id": str(audio_id)}, 201

@audio_routes.route('/audio/<audio_id>', methods=['DELETE'])
def delete_audio(audio_id):
    """
    Delete an audio file by its ID.
    """
    result = audio_collection.delete_one({"_id": ObjectId(audio_id)})
    if result.deleted_count == 0:
        return {"error": "Audio file not found"}, 404
    return {"message": "Audio file deleted successfully"}, 200

