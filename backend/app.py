from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'  # Change this in production

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

# Create database and add default admin user
with app.app_context():
    db.create_all()
    
    # Check if admin exists, otherwise create one
    if not User.query.filter_by(email="admin@example.com").first():
        hashed_password = bcrypt.generate_password_hash("password26948").decode('utf-8')
        admin_user = User(username="admin", email="admin@example.com", password_hash=hashed_password)
        db.session.add(admin_user)
        db.session.commit()

# Register Route
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password_hash=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        print("Invalid email or password")
        return jsonify({"error": "Invalid email or password"}), 401

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

if __name__ == '__main__':
    app.run(debug=True)
