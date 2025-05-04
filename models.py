# models.py
from flask_sqlalchemy import SQLAlchemy

# Initialize the db object here
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'  # <-- This sets the table name explicitly

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"
