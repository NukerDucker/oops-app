from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from modules.user import User
from modules.doctor import Doctor
from modules.receptionist import Receptionist
from modules.system import System

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()
system_service = System()

def init_auth_routes(blueprint, system, bcrypt):
    """Initialize auth routes with system and bcrypt dependencies"""
    global system_service, bcrypt_service
    system_service = system
    bcrypt_service = bcrypt
    return blueprint

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user_type = data.get('user_type')
    
    if not username or not password or not user_type:
        return jsonify({"error": "Username, password, and user type are required"}), 400
        
    if system_service.get_user_from_username(username):
        return jsonify({"error": "Username already taken"}), 400
        
    if user_type not in ["admin", "doctor", "receptionist"]:
        return jsonify({"error": "Invalid user type. Must be admin, doctor, or receptionist"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    if user_type == "admin":
        new_user = User(user_id, username, hashed_password, user_type="admin")
    elif user_type == "doctor":
        new_user = Doctor(user_id, username, hashed_password)
    elif user_type == "receptionist":
        new_user = Receptionist(user_id, username, hashed_password)
    
    success, message = system_service.add_user(new_user)
    
    if not success:
        return jsonify({"error": message}), 400

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = system_service.get_user_from_username(username)
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        print("Invalid username or password")
        return jsonify({"error": "Invalid username or password"}), 401

    
    access_token = create_access_token(identity=user.username)
    print(f"User {user.username} logged in")
    return jsonify({"access_token": access_token, "user": user.to_dict()}), 200

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": f"Hello, {current_username}! This is a protected route."}), 200
