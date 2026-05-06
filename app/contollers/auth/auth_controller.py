from flask import Blueprint,request,jsonify
#auth blueprint
auth = Blueprint('auth', __name__,url_prefix='api/v1/auth')

#user registration
@auth.route('/register',methods=['POST'])
def register_user():
    
    #storing request values
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact = data.get('contact')
    email = data.get('email')
    type = data.get('type')
    password = data.get('password')
    biography = data.get('biography', '') if type == "author" else ''
   
   if not first_name or last_name or not contact or not password or not email:
       return jsonify({
           "error": "All fields are required"}),
       