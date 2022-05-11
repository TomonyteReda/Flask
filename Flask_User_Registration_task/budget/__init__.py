# Import flask and template operators
from flask import Flask

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Import Bcrypt for password hashing
from flask_bcrypt import Bcrypt

# Import LoginManager for user session management
from flask_login import LoginManager

# Import Mail for mailing services
from flask_mail import Mail

# Import Admin for web service’s data management
from flask_admin import Admin


# Define the WSGI application object
app = Flask(__name__, instance_relative_config=True)

# Configurations
app.config.from_pyfile('config.py')

# Define Bcrypt instance
bcrypt = Bcrypt(app)

# Define Login Manager instance
login_manager = LoginManager(app)
login_manager.login_view = 'prisijungti'
login_manager.login_message_category = 'info'

# Define Mail instance
mail = Mail(app)

# Define Flask Admin instance
admin = Admin(app)

# Define the database object
db = SQLAlchemy(app)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
