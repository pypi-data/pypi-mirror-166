import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

cwd = os.getcwd()

# Application configuration
DEBUG = True
TESTING = False
SECRET_KEY = 'secret'
UPLOAD_PATH = os.path.join(cwd, 'instance', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

# Database configuration
DB_DIALECT = 'sqlite'
DB_DRIVER = os.environ.get('DB_DRIVER', 'mysql')
DB_USERNAME = os.environ.get('DB_USERNAME', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'root')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '3306')
DB_NAME = os.environ.get('DB_NAME', 'macrosignage')

if DB_DIALECT == 'sqlite':
    DB_URI = 'sqlite:///' + os.path.join(cwd, 'instance', 'macrosignage.db')
else:
    DB_URI = f'{DB_DIALECT}+{DB_DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# SQLAlchemy configuration
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
