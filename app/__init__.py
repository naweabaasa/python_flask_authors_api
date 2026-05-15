from flask import Flask
from app.extensions import db, migrate, jwt
from app.controllers.auth.auth_controller import auth
from app.controllers.users.user_controller import users

# Application factory function; 
# Organises the project so that it is easy to manage and maintain the code
# define the app instances within this function
def create_app():
    
#app instance
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
# registering the database instance on the app variable
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Importing and registering models
    from app.models.users import User
    from app.models.companies import Company
    from app.models.books import Book
    
    
    


# Registering blueprints  
    app.register_blueprint(auth)
    app.register_blueprint(users)
  
# Testing the application   
    @app.route("/")
    def home():
        return "Authors API Projecct setup"
    
    return app