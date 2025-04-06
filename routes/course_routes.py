from flask import Blueprint, request, jsonify
from config import course_collection
from bson import ObjectId
from pydantic import BaseModel, ValidationError, field_validator
from typing import Optional, List

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
    return jsonify({"course": course}), 200

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
    course_collection.insert_one(valid_course.model_dump())
    return {"message": "Course added successfully"}, 201

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
    result = course_collection.update_one({"id": course_id}, {"$set": valid_course.model_dump()})
    if result.matched_count == 0:
        return {"error": "Course not found"}, 404
    return {"message": "Course updated successfully"}, 200
