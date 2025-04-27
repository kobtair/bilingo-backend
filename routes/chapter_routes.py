from flask import Blueprint, request, jsonify
from config import chapter_collection, course_collection
from pydantic import BaseModel, ValidationError, field_validator
from typing import Optional
from bson import ObjectId

chapter_routes = Blueprint('chapter_routes', __name__)

# ChapterModel for validation
class ChapterModel(BaseModel):
    title: str
    course_id: str
    content: str
    audio_id: str
    description: str  # New field added
    order: int = 0    # new field: chapter order

    @field_validator("title")
    def title_non_empty(cls, v):
        if not v.strip():
            raise ValueError("Title must be a non-empty string")
        return v.strip()

    @field_validator("course_id")
    def course_id_non_empty(cls, v):
        if not v.strip():
            raise ValueError("Course ID must be a non-empty string")
        return v.strip()

    @field_validator("content")
    def content_non_empty(cls, v):
        if not v.strip():
            raise ValueError("Content must be a non-empty string")
        return v.strip()

    @field_validator("audio_id")
    def audio_id_non_empty(cls, v):
        if not v.strip():
            raise ValueError("Audio ID must be a non-empty string")
        return v.strip()

    @field_validator("description")
    def description_non_empty(cls, v):
        if not v.strip():
            raise ValueError("Description must be a non-empty string")
        return v.strip()

@chapter_routes.route('/courses/<course_id>/chapters', methods=['GET'])
def get_chapters(course_id):
    """
    Get all chapters for a specific course.
    """
    chapters = list(chapter_collection.find({"course_id": course_id}))
    for chapter in chapters:
        chapter['_id'] = str(chapter['_id'])  # Convert ObjectId to string
    return jsonify(chapters), 200

@chapter_routes.route('/courses/<course_id>/chapters', methods=['POST'])
def add_chapter(course_id):
    """
    Add a new chapter to a specific course.
    """
    chapter_data = request.get_json()
    chapter_data['course_id'] = course_id  # Ensure course_id is set
    try:
        valid_chapter = ChapterModel.model_validate(chapter_data)
    except ValidationError as e:
        return {"error": e.errors()}, 400
    result = chapter_collection.insert_one(valid_chapter.model_dump())
    # Update the chapters array in the respective course
    course_collection.update_one(
        {"_id": course_id},
        {"$push": {"chapters": str(result.inserted_id)}}
    )
    return jsonify(chapter_data), 201

@chapter_routes.route('/chapters/<chapter_id>', methods=['GET'])
def get_chapter_by_id(chapter_id):
    """
    Get a chapter by its ID.
    """
    chapter = chapter_collection.find_one({"id": chapter_id})
    if not chapter:
        try:
            chapter = chapter_collection.find_one({"_id": ObjectId(chapter_id)})
        except Exception:
            chapter = None
    if not chapter:
        return {"error": "Chapter not found"}, 404
    chapter['_id'] = str(chapter['_id'])  # Convert ObjectId to string
    return jsonify(chapter), 200

@chapter_routes.route('/chapters/<chapter_id>', methods=['PATCH'])
def update_chapter(chapter_id):
    """
    Update a chapter by its ID.
    """
    chapter_data = request.get_json()
    try:
        valid_chapter = ChapterModel.model_validate(chapter_data)
    except ValidationError as e:
        return {"error": e.errors()}, 400
    result = chapter_collection.update_one(
        {"_id": ObjectId(chapter_id)},
        {"$set": valid_chapter.model_dump()}
    )
    if result.matched_count == 0:
        return {"error": "Chapter not found"}, 404
    return {"message": "Chapter updated successfully"}, 200

@chapter_routes.route('/chapters/<chapter_id>', methods=['DELETE'])
def delete_chapter(chapter_id):
    """
    Delete a chapter by its ID.
    """
    # Retrieve chapter to get course_id before deletion
    chapter = chapter_collection.find_one({"_id": ObjectId(chapter_id)})
    if not chapter:
        return {"error": "Chapter not found"}, 404
    course_id = chapter.get("course_id")
    result = chapter_collection.delete_one({"_id": ObjectId(chapter_id)})
    if result.deleted_count == 0:
        return {"error": "Chapter not found"}, 404
    # Remove the chapter id from the respective course's chapters array
    course_collection.update_one(
        {"_id": course_id},
        {"$pull": {"chapters": chapter_id}}
    )
    return {"message": "Chapter deleted successfully"}, 200

@chapter_routes.route('/courses/<course_id>/chapters/reorder', methods=['POST'])
def reorder_chapters(course_id):
    """
    Reorder chapters within a course.
    """
    data = request.get_json()
    chapter_ids = data.get("chapterIds")
    if not isinstance(chapter_ids, list):
        return {"error": "Invalid chapterIds format"}, 400
    for index, chapter_id in enumerate(chapter_ids):
        chapter_collection.update_one(
            {"_id": ObjectId(chapter_id), "course_id": course_id},
            {"$set": {"order": index}}
        )
    return {"message": "Chapters reordered successfully"}, 200
