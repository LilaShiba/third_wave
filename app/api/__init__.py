# app/api/__init__.py
# Moved inside to avoid circular imports
from .sensors import register_sensors_routes
from .actuators import register_actuators_routes
from flask import Blueprint

api_bp = Blueprint('api_bp', __name__)

register_sensors_routes(api_bp)
register_actuators_routes(api_bp)


