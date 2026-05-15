from flask import Blueprint, request, jsonify
from app.status_codes import (HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_200_OK)
import validators
from app.models.users import User
from app.extensions import db, bcrypt
from  flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity, create_refresh_token

# auth blueprint
auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth.route('/register', methods=['POST'])
def register_user():

    # DEBUG (only for testing - remove later if you want)
    print("RAW:", request.data)
    print("JSON:", request.get_json(silent=True))

    # get JSON data
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), HTTP_400_BAD_REQUEST

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact = data.get('contact')
    email = data.get('email')
    user_type = data.get('type', 'author')
    password = data.get('password')
    biography = data.get('biography', '') if user_type == "author" else ''

    if not first_name or not last_name or not contact or not password or not email:
        return jsonify({"error": "All fields are required"}), HTTP_400_BAD_REQUEST

    if user_type == 'author' and not biography:
        return jsonify({"error": "Enter your author biography"}), HTTP_400_BAD_REQUEST

    if len(password) < 8:
        return jsonify({"error": "Password is too short"}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({"error": "Email is not valid"}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email address already in use"}), HTTP_409_CONFLICT

    if User.query.filter_by(contact=contact).first():
        return jsonify({"error": "Contact already in use"}), HTTP_409_CONFLICT

    try:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            password=hashed_password,
            email=email,
            contact=contact,
            biography=biography,
            user_type=user_type
        )

        db.session.add(new_user)
        db.session.commit()

        username = new_user.get_full_name()

        return jsonify({
            "message": f"{username} has been successfully created as an {new_user.user_type}",
            "user": {
                "id": new_user.id,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email,
                "contact": new_user.contact,
                "type": new_user.user_type,
                "biography": new_user.biography,
                "created_at": new_user.created_at
            }
        }), HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    




#User login
@auth.post('/login',)
def login():

    email = request.json.get('email')
    password = request.json.get('password')


    try:
        if not email or not password:
            return jsonify({"Message": "Email and password are required"}), HTTP_400_BAD_REQUEST

        user = User.query.filter_by(email=email).first()

        if user:
            is_correct_password = bcrypt.check_password_hash(user.password, password)

            if is_correct_password:
                access_token = create_access_token(identity=str(user.id))
                refresh_token = create_refresh_token(identity=str(user.id))

                return jsonify({
                    'user': {
                        "id": user.id,
                        "username": user.get_full_name(),
                        'email': user.email,
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                        'type': user.user_type
                        
                    },
                    'message': "You have successfully logged into your account"
                }),HTTP_200_OK
            
            else:
                return jsonify({"Message": "Invalid password"}), HTTP_401_UNAUTHORIZED

        else:
            return jsonify({"Message": "Invalid email addresss"}), HTTP_401_UNAUTHORIZED

    except Exception as e: 
        return jsonify({
            "error": str(e)
            }), HTTP_500_INTERNAL_SERVER_ERROR
    


@auth.route("/token/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = int(get_jwt_identity())     # convert string back to integer
    access_token = create_access_token(identity=str(user_id))     # store as string again
    return jsonify({"access_token":access_token})

