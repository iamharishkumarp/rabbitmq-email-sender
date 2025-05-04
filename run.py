# app.py
from flask import Flask
from flask_bcrypt import Bcrypt
from models import db  # Import db from models
from app.routes import email_bp  # Import routes
import os

# Initialize Flask app
app = Flask(__name__)

# Configure app with your database URI
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'postgresql://postgres:root@db/postgres')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db and bcrypt
bcrypt = Bcrypt(app)
db.init_app(app)  # Ensure db is initialized with the app

# Register blueprints
app.register_blueprint(email_bp, url_prefix='/email')

# Create tables if they don't exist yet
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
