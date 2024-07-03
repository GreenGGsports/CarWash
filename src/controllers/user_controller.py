from src.models.user_model import UserModel
from sqlalchemy.orm import Session
from flask import Blueprint, request, jsonify
import jwt
from functools import wraps


SECRET_KEY = 'your_secret_key'

user_ctrl = Blueprint('user_ctrl', __name__, url_prefix='/user')


# Function to generate JWT token
def generate_token(user_id):
    token = jwt.encode({'user_id': user_id}, SECRET_KEY, algorithm='HS256')
    return token.decode('utf-8')

# Decorator function to verify JWT token
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Missing token'}), 401
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            
            # Optionally, fetch additional user data if needed
            user = UserModel.query.get(user_id)
            
            # Attach user_id to the request object for use in route functions
            request.user_id = user_id
            request.user = user  # Optionally attach user object
            
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        
        return func(*args, **kwargs)
    
    return decorated_function

@user_ctrl.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_name = data.get('user_name')
    password = data.get('password')

    user = UserModel.login(user_name=user_name, password=password)
    if user:
        token = generate_token(user.id)
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
    

@user_ctrl.route('/login', methods=['POST'])
def add_user(session: Session ,user_name, password):
    msg = ''
    if UserModel.check_name_taken(user_name=user_name):
        
        msg = 'Name is taken try with another username' 
    
    else:
        UserModel.add_user(session=session, user_name=user_name, password=password)
        msg = 'Sucess!'
    
    return msg 