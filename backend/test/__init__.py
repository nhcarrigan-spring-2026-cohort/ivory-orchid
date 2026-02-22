import sys
import os
import pytest

os.environ["FLASK_TESTING"] = "true"
os.environ["TESTING"] = "true"

sys.path.append("..")
from app import create_app, db

# Create a test app with in-memory SQLite database
test_config = {
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    'TESTING': True
}

app = create_app(test_config=test_config)

@pytest.fixture
def client():
	"""Create a test client for the Flask app."""
	with app.app_context():
		db.create_all()
		yield app.test_client()
		db.session.remove()
		db.drop_all()

@pytest.fixture
def runner():
	"""Create a CLI runner for the Flask app."""
	return app.test_cli_runner()
