from flask import Blueprint
from .auth_routes import auth_routes
from .user_routes import user_routes
from .admin_routes import admin_routes
from .leaderboard_routes import leaderboard_routes
from .course_routes import course_routes   
from .analyze import analyze_routes        
from .stats_routes import stats_routes
from .audio_routes import audio_routes
from .chapter_routes import chapter_routes
from .progress_routes import progress_routes
from .dummy_analyze import dummy_analyze_routes

routes = Blueprint('routes', __name__)

# Register individual blueprints
routes.register_blueprint(auth_routes)
routes.register_blueprint(user_routes)
routes.register_blueprint(admin_routes)
routes.register_blueprint(leaderboard_routes)
routes.register_blueprint(course_routes)         
routes.register_blueprint(analyze_routes)        
routes.register_blueprint(stats_routes)
routes.register_blueprint(audio_routes)
routes.register_blueprint(chapter_routes)
routes.register_blueprint(progress_routes)
routes.register_blueprint(dummy_analyze_routes)