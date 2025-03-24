from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from modules.system import System

users_bp = Blueprint('users', __name__)
system_service = System()

def init_users_routes(blueprint, system):
    """Initialize user routes with system dependency"""
    global system_service
    system_service = system
    return blueprint

@users_bp.route('/api/user-data', methods=['GET'])
@jwt_required()
def get_user_data():
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict())

@users_bp.route('/api/users', methods=['GET'])
@jwt_required()
def get_all_users():
    # Only allow admin to see all users
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    if user.user_type != "admin":
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify([u.to_dict() for u in users])

@users_bp.route('/api/users/doctors', methods=['GET'])
@jwt_required()
def get_doctors():
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    if not user or user.user_type not in ["admin", "receptionist"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get all users with doctor role
    doctors = [
        {
            'id': u.id,
            'name': u.username
        }
        for u in system_service._users.values() 
        if u.user_type == "doctor"
    ]
    
    return jsonify(doctors), 200