"""
Database models for the Ivory Orchid application.
Uses SQLAlchemy ORM with Flask-SQLAlchemy integration.
"""
from datetime import datetime
from . import db


class User(db.Model):
    """
    User model for user registration and profile management.
    
    Fields:
    - id: Primary key (auto-generated)
    - name: User's full name (required)
    - email: User's email address (required, unique)
    - age: User's age (required, must be positive integer)
    - created_at: Timestamp when user was created
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    age = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.id}: {self.email}>'
    
    def to_dict(self):
        """Convert user object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'created_at': self.created_at.isoformat()
        }


class Contact(db.Model):
    """
    Contact model for storing contact form submissions.
    
    Fields:
    - id: Primary key (auto-generated)
    - name: Submitter's name (required)
    - email: Submitter's email (required)
    - message: Contact message (required)
    - created_at: Timestamp when submission was received
    """
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Contact {self.id}: {self.email}>'
    
    def to_dict(self):
        """Convert contact object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'message': self.message,
            'created_at': self.created_at.isoformat()
        }
