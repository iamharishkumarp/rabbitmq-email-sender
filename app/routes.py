import bcrypt
from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from publisher import publish_email  
from models import db, User

# Initialize Flask-Bcrypt
bcrypt = Bcrypt()

# Email Blueprint
email_bp = Blueprint('email', __name__)


# Signup route - User Registration
@email_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required!"}), 400

    # Check if the user already exists in the database
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered!"}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create new user and store it in the database
    new_user = User(email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

@email_bp.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()

    to_email = data.get('to')
    subject = data.get('subject')
    message = data.get('message')

    if not all([to_email, subject, message]):
        return jsonify({"error": "Missing fields"}), 400

    # Publish to RabbitMQ
    publish_email(to_email, subject, message)

    return jsonify({"message": "Email sent successfully"}), 200

# Login route
@email_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_email = data.get('email')
    user_password = data.get('password')

    # Validate input
    if not user_email or not user_password:
        return jsonify({"error": "Email and password are required!"}), 400

    # Check if the user exists in the database
    user = User.query.filter_by(email=user_email).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, user_password):
        return jsonify({"error": "Invalid email or password!"}), 401

    # Send login notification email via RabbitMQ
    subject = "Login Notification"
    message = "You have successfully logged in."
    publish_email(user_email, subject, message)

    return jsonify({"message": "Login successful and email notification sent."}), 200
    

# Change Password route
@email_bp.route('/change-password', methods=['POST'])
def change_password():
    data = request.get_json()
    user_email = data.get('email')
    new_password = data.get('new_password')

    if not user_email or not new_password:
        return jsonify({"error": "Email and new password are required!"}), 400

    # Check if the user exists in the database
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({"error": "User not found!"}), 404

    # Hash the new password and update it in the database
    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user.password_hash = hashed_password
    db.session.commit()

    # Send password change notification email via RabbitMQ
    subject = "Password Change Notification"
    message = "Your password has been successfully changed."
    publish_email(user_email, subject, message)

    return jsonify({"message": "Password changed and email notification sent."}), 200
    

# Logout route
@email_bp.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    user_email = data.get('email')

    if not user_email:
        return jsonify({"error": "Email is required!"}), 400

    # Send logout notification email via RabbitMQ
    subject = "Logout Notification"
    message = "You have successfully logged out."
    publish_email(user_email, subject, message)

    return jsonify({"message": "Logged out and email notification sent."}), 200
