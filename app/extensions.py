
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# creating a new database instance
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()