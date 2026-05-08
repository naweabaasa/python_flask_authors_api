from flask import Blueprint, request, jsonify
#  jsonify helps to return responses
# request helps get data from the user
from app.status_codes  import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR
import validators
# validators help to keep consistence of data
from app.models.users import User
from app.extensions import db
from app.extensions import bcrypt
# bcrypt helps to work with the security for password


# auth blueprint
auth = Blueprint('auth', __name__,url_prefix='api/v1/auth')

# user registration
# routes handle incoming requests
@auth.route('/register', methods=['POST'])
def register_user():
    
# storing request values
    data = request.json
    print(data)
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact = data.get('contact')
    email = data.get('email')
    type = data.get('type')
    password = data.get('password')
    biography = data.get('biography', '') if type =="author" else ''
    
    
# validations of the incoming request; required data must be submitted
    
    if not first_name or last_name or not contact or not password or not email:
        return jsonify({"error:" "All fields are required"}), HTTP_400_BAD_REQUEST
# status codes are optional
    
    
    if type == 'author' and not biography:
        return jsonify({"error:" "Enter your author biography"}), HTTP_400_BAD_REQUEST
    
    if len(password) < 8:
        return jsonify({"error:" "Password is too short"}), HTTP_400_BAD_REQUEST
    
    if not validators.email(email): 
        return jsonify({"error:" "Email is not valid"}), HTTP_400_BAD_REQUEST
    
    
# constaint check
# We make constraints using the models
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error:" "Email address in use"}), HTTP_409_CONFLICT    
    
    if User.query.filter_by(contact=contact).first() is not None:
        return jsonify({"error:" "Contact in use"}), HTTP_409_CONFLICT 
    
# Adding functionality of the user
    try:
        
# hashing the password for security
        hashed_password = bcrypt.generate_password_hash(password)
       
# Creating a new user   
        new_user = User(first_name=first_name, last_name=last_name, password=hashed_password, email=email, contact=contact, biography=biography, user_type=type)
# saving the user
        db.session.add(new_user)    
        db.session.commit()
        
# username
        username = new_user.get_full_name()
        
        return jsonify({
            'message': username + "has been successfully created as an" + new_user.user_type,
            'user' :{
                "id" : new_user.id,
                "first__name" : new_user.first_name,
                "last_name" : new_user.last_name,
                "email" : new_user.email,
                "contact" : new_user.contact,
                "type" : new_user.type,
                "biography" : new_user.biography,
                "created_at" : new_user.created _at,
            }
        })
        
# helps to roll back when there's an error
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}), HTTP_500_INTERNAL_SERVER_ERROR     
    
    