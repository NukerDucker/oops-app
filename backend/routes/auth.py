from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

# These will be imported from app.py
users = []

def find_user_by_username(username):
    for user in users:
        if user.username == username:
            return user
    return None

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
        
    if find_user_by_username(username):
        return jsonify({"error": "Username already taken"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user_id = len(users) + 1  # Simple ID generation
    from modules.user import User
    new_user = User(user_id, username, hashed_password)
    users.append(new_user)

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = find_user_by_username(username)
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        print("Invalid username or password")
        return jsonify({"error": "Invalid username or password"}), 401

    # Create JWT token - store just the username as identity
    access_token = create_access_token(identity=user.username)
    print(f"User {user.username} logged in")
    return jsonify({"access_token": access_token, "user": user.to_dict()}), 200

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_username = get_jwt_identity()
    return jsonify({"message": f"Hello, {current_username}! This is a protected route."}), 200