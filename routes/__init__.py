from flask import Blueprint
from .auth_routes import auth_routes
from .user_routes import user_routes
from .admin_routes import admin_routes
from .leaderboard_routes import leaderboard_routes
from .course_routes import course_routes        # added course routes
from .analyze import analyze_routes        # added analyze route

routes = Blueprint('routes', __name__)

# Register individual blueprints
routes.register_blueprint(auth_routes)
routes.register_blueprint(user_routes)
routes.register_blueprint(admin_routes)
routes.register_blueprint(leaderboard_routes)
routes.register_blueprint(course_routes)         
routes.register_blueprint(analyze_routes)        
