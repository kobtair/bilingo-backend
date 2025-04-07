from flask import Blueprint, jsonify
from datetime import datetime
from config import user_collection, course_collection, audio_collection, admin_collection

stats_routes = Blueprint('stats_routes', __name__)

@stats_routes.route('/stats/dashboard', methods=['GET'])
def dashboard():
    first_day = datetime.today().replace(day=1)
    
    totalUsers = user_collection.count_documents({})
    totalCourses = course_collection.count_documents({})
    totalAudioFiles = audio_collection.count_documents({})
    totalAdmins = admin_collection.count_documents({})
    
    newUsersThisMonth = user_collection.count_documents({'createdAt': {'$gte': first_day}})
    newCoursesThisMonth = course_collection.count_documents({'createdAt': {'$gte': first_day}})
    newAudioFilesThisMonth = audio_collection.count_documents({'createdAt': {'$gte': first_day}})
    newAdminsThisMonth = admin_collection.count_documents({'createdAt': {'$gte': first_day}})
    
    stats_data = {
        "totalUsers": totalUsers,
        "totalCourses": totalCourses,
        "totalAudioFiles": totalAudioFiles,
        "totalAdmins": totalAdmins,
        "newUsersThisMonth": newUsersThisMonth,
        "newCoursesThisMonth": newCoursesThisMonth,
        "newAudioFilesThisMonth": newAudioFilesThisMonth,
        "newAdminsThisMonth": newAdminsThisMonth,
    }
    return jsonify(stats_data)

