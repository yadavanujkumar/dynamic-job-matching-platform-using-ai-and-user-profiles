from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps

# Mock database (replace with actual database integration)
mock_users_db = {}

# Secret key for JWT (use a secure key in production)
SECRET_KEY = "your_secret_key"

# Blueprint for user routes
user_routes = Blueprint('user_routes', __name__)

# Helper function to authenticate token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = mock_users_db.get(data['user_id'])
            if not current_user:
                return jsonify({'message': 'User not found!'}), 401
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# User registration route
@user_routes.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({'message': 'Invalid input!'}), 400

    email = data['email']
    if email in [user['email'] for user in mock_users_db.values()]:
        return jsonify({'message': 'Email already exists!'}), 409

    user_id = str(uuid.uuid4())
    hashed_password = generate_password_hash(data['password'], method='sha256')
    mock_users_db[user_id] = {
        'user_id': user_id,
        'name': data['name'],
        'email': email,
        'password': hashed_password,
        'profile': {}
    }

    return jsonify({'message': 'User registered successfully!', 'user_id': user_id}), 201

# User login route
@user_routes.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Invalid input!'}), 400

    email = data['email']
    password = data['password']
    user = next((user for user in mock_users_db.values() if user['email'] == email), None)

    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid email or password!'}), 401

    token = jwt.encode({
        'user_id': user['user_id'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({'message': 'Login successful!', 'token': token}), 200

# Fetch user details route
@user_routes.route('/profile', methods=['GET'])
@token_required
def get_user_profile(current_user):
    return jsonify({
        'user_id': current_user['user_id'],
        'name': current_user['name'],
        'email': current_user['email'],
        'profile': current_user['profile']
    }), 200

# Update user profile route
@user_routes.route('/profile', methods=['PUT'])
@token_required
def update_user_profile(current_user):
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Invalid input!'}), 400

    current_user['profile'].update(data)
    return jsonify({'message': 'Profile updated successfully!', 'profile': current_user['profile']}), 200