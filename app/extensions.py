
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# creating a new database instance
db = SQLAlchemy()
migrate = Migrate()