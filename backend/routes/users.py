from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

users_bp = Blueprint('users', __name__)

# These will be imported from app.py
users = []

def find_user_by_username(username):
    for user in users:
        if user.username == username:
            return user
    return None

@users_bp.route('/api/user-data', methods=['GET'])
@jwt_required()
def get_user_data():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict())

@users_bp.route('/api/users', methods=['GET'])
@jwt_required()
def get_all_users():
    # Only allow admin to see all users
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    if user.user_type != "admin":
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify([u.to_dict() for u in users])