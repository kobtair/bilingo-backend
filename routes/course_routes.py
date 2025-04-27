from flask import Blueprint, request, jsonify
from config import course_collection
from bson import ObjectId
from pydantic import BaseModel, ValidationError, field_validator
from typing import Optional, List
import uuid  # new import

course_routes = Blueprint('course_routes', __name__)

# New ChapterModel for course chapters
class ChapterModel(BaseModel):
    title: str
    description: Optional[str] = None
    content: str
    audio_file: str

    @field_validator("title")
    def chapter_title_non_empty(cls, v):
        if not v.strip():
            raise ValueError("Chapter title must be a non-empty string")
        return v.strip()

# Updated CourseModel with new fields and chapters
class CourseModel(BaseModel):
    title: str
    language: str  # new field
    dialect: str   # new field for dialect
    description: Optional[str] = None
    chapters: List[ChapterModel] = []  # new field with default empty list

    @field_validator("title")
    def title_non_empty(cls, v):
        if not v.strip():
            raise ValueError("Title must be a non-empty string")
        return v.strip()

    @field_validator("language")
    def language_non_empty(cls, v):
        if not v.strip():
            raise ValueError("Language must be a non-empty string")
        return v.strip()
    
    @field_validator("dialect")
    def dialect_non_empty(cls, v):
        if not v.strip():
            raise ValueError("Dialect must be a non-empty string")
        return v.strip()

    @field_validator("description", mode="before")
    def description_strip(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v

@course_routes.route('/courses', methods=['GET'])
def get_courses():
    """
    Get all courses from the database.
    """
    courses = list(course_collection.find())
    for course in courses:
        for key in list(course.keys()):
            if isinstance(course[key], bytes):
                course[key] = course[key].decode('utf-8')
        del course['_id']
    return jsonify(courses), 200

@course_routes.route('/courses/<course_id>', methods=['GET'])
def get_course(course_id):
    """
    Get a specific course by ID from the database.
    """
    course = course_collection.find_one({"id": course_id})
    if not course:
        return jsonify({"error": "Course not found"}), 404
    course['_id'] = str(course['_id'])
    return jsonify(course), 200

@course_routes.route('/courses', methods=['POST'])
def add_course():
    """
    Add a new course to the database.
    """
    course_data = request.get_json()
    try:
        valid_course = CourseModel.model_validate(course_data)
    except ValidationError as e:
        return {"error": e.errors()}, 400
    new_course_data = valid_course.model_dump()
    new_id = str(uuid.uuid4())  # generate unique id
    new_course_data["id"] = new_id  # add unique id to course data
    new_course = course_collection.insert_one(new_course_data)
    new_course_data['_id'] = str(new_course.inserted_id)  # convert ObjectId to string
    # Return the new course document which includes the 'id'
    return jsonify(new_course_data), 201

@course_routes.route('/courses/<course_id>', methods=['PUT'])
def update_course(course_id):
    """
    Update an existing course in the database.
    """
    course_data = request.get_json()
    try:
        valid_course = CourseModel.model_validate(course_data)
    except ValidationError as e:
        return {"error": e.errors()}, 400
    update_data = valid_course.model_dump()
    update_data["id"] = course_id  # enforce unique id remains unchanged
    result = course_collection.update_one({"id": course_id}, {"$set": update_data})
    if result.matched_count == 0:
        return {"error": "Course not found"}, 404
    update_course = course_collection.find_one({"id": course_id})
    update_course['_id'] = str(update_course['_id'])
    return jsonify(update_course), 200

@course_routes.route('/courses/<course_id>', methods=['DELETE'])
def delete_course(course_id):
    """
    Delete an existing course from the database.
    """
    course = course_collection.find_one({"id": course_id})
    if not course:
        return jsonify({"error": "Course not found"}), 404
    course_collection.delete_one({"id": course_id})
    return jsonify({"message": "Course deleted"}), 200
