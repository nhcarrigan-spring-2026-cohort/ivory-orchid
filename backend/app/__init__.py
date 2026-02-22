import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance
db = SQLAlchemy()

def create_app(test_config=None):
    """Application factory pattern for Flask app initialization"""
    app = Flask(__name__, template_folder="../../frontend/templates")
    
    # Configure database
    if test_config is None:
        # Development/Production configuration
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    else:
        # Testing configuration (in-memory SQLite)
        app.config.update(test_config)
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database with the app
    db.init_app(app)
    
    # Import models to register them with SQLAlchemy
    from . import models
    
    # Register blueprints
    from . import dataEndpoints, static
    app.register_blueprint(dataEndpoints.data_bp)
    app.register_blueprint(static.static_bp)
    
    # Register error handlers
    app.register_error_handler(404, static.load_static)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

# For backward compatibility with existing code that imports 'app'
app = create_app()
