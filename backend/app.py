from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from modules.user import User

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# JWT configuration
app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'  # Change this in production

# Initialize extensions
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# In-memory user storage
users = []

# Add default admin user
hashed_password = bcrypt.generate_password_hash("password26948").decode('utf-8')
admin_user = User(1, "Admin", hashed_password, "admin")
users.append(admin_user)

# Helper function to find user by username
def find_user_by_username(username):
    for user in users:
        if user.username == username:
            return user
    return None

# Register Route
@app.route('/register', methods=['POST'])
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
    new_user = User(user_id, username, hashed_password)
    users.append(new_user)

    return jsonify({"message": "User registered successfully"}), 201

# Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = find_user_by_username(username)
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        print("Invalid username or password")
        return jsonify({"error": "Invalid username or password"}), 401

    # Create JWT token
    access_token = create_access_token(identity={"id": user.id, "username": user.username})
    print(f"User {user.username} logged in")
    return jsonify({"access_token": access_token}), 200

# Protected Route
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Hello, {current_user['username']}! This is a protected route."}), 200

@app.route('/api/user-data', methods=['GET'])
def get_user_data():
    # Check if user is authenticated
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Get user from database
    user_id = session['user_id']
    user = User.query.get(user_id)  # Using SQLAlchemy as an example
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Format user data similar to your existing JSON structure
    user_data = {
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'profile_image_directory': user.profile_image_path,
        'allow_access': [
            {'access': access.name, 'access_link': access.link}
            for access in user.access_permissions
        ],
        'tasks': [task.to_dict() for task in user.tasks],
        'weekly_tasks': [task.to_dict() for task in user.weekly_tasks],
        'emergency_tasks': [task.to_dict() for task in user.emergency_tasks]
    }
    
    return jsonify(user_data)

if __name__ == '__main__':
    app.run(debug=True)
