from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Enable CORS
from .config import SQLALCHEMY_DATABASE_URI
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Add configurations
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "your_secret_key"

    # Define the upload folder (adjust path as needed)
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

    db.init_app(app)
    CORS(app)  # Enable CORS for frontend requests

    from .routes import main
    app.register_blueprint(main)

    return app
