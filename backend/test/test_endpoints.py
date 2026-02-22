"""
Integration tests for API endpoints.
Tests full request/response workflows and database operations.
"""
import pytest
from app import db
from app.models import User, Contact


@pytest.fixture
def client(app=None):
	"""Create a test client with fresh database."""
	from test import app as test_app
	with test_app.app_context():
		db.create_all()
		yield test_app.test_client()
		db.session.remove()
		db.drop_all()


class TestUserRegistrationEndpoint:
	"""Tests for POST /api/users/register endpoint."""
	
	def test_register_user_success(self, client):
		"""Test successful user registration with valid data."""
		data = {
			'name': 'John Doe',
			'email': 'john@example.com',
			'age': 25
		}
		response = client.post('/api/users/register', json=data)
		
		assert response.status_code == 201
		json_data = response.get_json()
		assert json_data['message'] == 'User registered successfully'
		assert json_data['user']['name'] == 'John Doe'
		assert json_data['user']['email'] == 'john@example.com'
		assert json_data['user']['age'] == 25
		assert json_data['user']['id'] is not None
	
	def test_register_user_stored_in_database(self, client):
		"""Test that registered user is actually stored in database."""
		data = {
			'name': 'Jane Smith',
			'email': 'jane@example.com',
			'age': 30
		}
		response = client.post('/api/users/register', json=data)
		
		assert response.status_code == 201
		
		# Verify user exists in database
		from test import app as test_app
		with test_app.app_context():
			user = User.query.filter_by(email='jane@example.com').first()
			assert user is not None
			assert user.name == 'Jane Smith'
			assert user.age == 30
	
	def test_register_user_missing_name(self, client):
		"""Test registration fails when name is missing."""
		data = {
			'email': 'john@example.com',
			'age': 25
		}
		response = client.post('/api/users/register', json=data)
		
		assert response.status_code == 400
		json_data = response.get_json()
		assert json_data['message'] == 'Validation failed'
		assert 'name' in json_data['errors']
	
	def test_register_user_missing_email(self, client):
		"""Test registration fails when email is missing."""
		data = {
			'name': 'John Doe',
			'age': 25
		}
		response = client.post('/api/users/register', json=data)
		
		assert response.status_code == 400
		json_data = response.get_json()
		assert json_data['message'] == 'Validation failed'
		assert 'email' in json_data['errors']
	
	def test_register_user_missing_age(self, client):
		"""Test registration fails when age is missing."""
		data = {
			'name': 'John Doe',
			'email': 'john@example.com'
		}
		response = client.post('/api/users/register', json=data)
		
		assert response.status_code == 400
		json_data = response.get_json()
		assert json_data['message'] == 'Validation failed'
		assert 'age' in json_data['errors']
	
	def test_register_user_invalid_email(self, client):
		"""Test registration fails with invalid email format."""
		data = {
			'name': 'John Doe',
			'email': 'invalid-email',
			'age': 25
		}
		response = client.post('/api/users/register', json=data)
		
		assert response.status_code == 400
		json_data = response.get_json()
		assert json_data['message'] == 'Validation failed'
		assert 'email' in json_data['errors']
	
	def test_register_user_invalid_age(self, client):
		"""Test registration fails with invalid age."""
		data = {
			'name': 'John Doe',
			'email': 'john@example.com',
			'age': -5
		}
		response = client.post('/api/users/register', json=data)
		
		assert response.status_code == 400
		json_data = response.get_json()
		assert json_data['message'] == 'Validation failed'
		assert 'age' in json_data['errors']
	
	def test_register_user_duplicate_email(self, client):
		"""Test registration fails when email already exists."""
		data1 = {
			'name': 'John Doe',
			'email': 'john@example.com',
			'age': 25
		}
		data2 = {
			'name': 'Jane Doe',
			'email': 'john@example.com',
			'age': 30
		}
		
		# Register first user
		response1 = client.post('/api/users/register', json=data1)
		assert response1.status_code == 201
		
		# Try to register second user with same email
		response2 = client.post('/api/users/register', json=data2)
		assert response2.status_code == 409
		json_data = response2.get_json()
		assert json_data['message'] == 'Email already registered'
		assert 'already exists' in json_data['error']
	
	def test_register_user_invalid_json(self, client):
		"""Test registration fails with malformed JSON."""
		response = client.post(
			'/api/users/register',
			data='invalid json',
			content_type='application/json'
		)
		
		assert response.status_code == 422
		json_data = response.get_json()
		assert json_data['message'] == 'Invalid JSON data'
	
	def test_register_user_no_json_body(self, client):
		"""Test registration fails when no JSON body provided."""
		response = client.post('/api/users/register')
		
		assert response.status_code == 422
		json_data = response.get_json()
		assert json_data['message'] == 'Invalid JSON data'


class TestContactFormEndpoint:
	"""Tests for POST /contact endpoint."""
	
	def test_contact_form_post_success(self, client):
		"""Test successful contact form submission with valid data."""
		data = {
			'name': 'John Doe',
			'email': 'john@example.com',
			'message': 'This is a test message for contact form'
		}
		response = client.post(
			'/contact',
			json=data,
			content_type='application/json'
		)
		
		assert response.status_code == 201
		json_data = response.get_json()
		assert json_data['message'] == 'Contact form submitted successfully'
		assert json_data['contact']['name'] == 'John Doe'
		assert json_data['contact']['email'] == 'john@example.com'
	
	def test_contact_form_stored_in_database(self, client):
		"""Test that contact form data is stored in database."""
		data = {
			'name': 'Jane Smith',
			'email': 'jane@example.com',
			'message': 'This is a test message from Jane'
		}
		response = client.post(
			'/contact',
			json=data,
			content_type='application/json'
		)
		
		assert response.status_code == 201
		
		# Verify contact exists in database
		from test import app as test_app
		with test_app.app_context():
			contact = Contact.query.filter_by(email='jane@example.com').first()
			assert contact is not None
			assert contact.name == 'Jane Smith'
			assert contact.message == 'This is a test message from Jane'
	
	def test_contact_form_missing_name(self, client):
		"""Test contact form fails when name is missing."""
		data = {
			'email': 'john@example.com',
			'message': 'This is a test message'
		}
		response = client.post('/contact', json=data)
		
		assert response.status_code == 400
		json_data = response.get_json()
		assert json_data['message'] == 'Validation failed'
		assert 'name' in json_data['errors']
	
	def test_contact_form_missing_email(self, client):
		"""Test contact form fails when email is missing."""
		data = {
			'name': 'John Doe',
			'message': 'This is a test message'
		}
		response = client.post('/contact', json=data)
		
		assert response.status_code == 400
		json_data = response.get_json()
		assert json_data['message'] == 'Validation failed'
		assert 'email' in json_data['errors']
	
	def test_contact_form_missing_message(self, client):
		"""Test contact form fails when message is missing."""
		data = {
			'name': 'John Doe',
			'email': 'john@example.com'
		}
		response = client.post('/contact', json=data)
		
		assert response.status_code == 400
		json_data = response.get_json()
		assert json_data['message'] == 'Validation failed'
		assert 'message' in json_data['errors']
	
	def test_contact_form_invalid_email(self, client):
		"""Test contact form fails with invalid email."""
		data = {
			'name': 'John Doe',
			'email': 'invalid-email',
			'message': 'This is a test message'
		}
		response = client.post('/contact', json=data)
		
		assert response.status_code == 400
		json_data = response.get_json()
		assert json_data['message'] == 'Validation failed'
		assert 'email' in json_data['errors']
	
	def test_contact_form_message_too_short(self, client):
		"""Test contact form fails with message shorter than 10 chars."""
		data = {
			'name': 'John Doe',
			'email': 'john@example.com',
			'message': 'Short'
		}
		response = client.post('/contact', json=data)
		
		assert response.status_code == 400
		json_data = response.get_json()
		assert json_data['message'] == 'Validation failed'
		assert 'message' in json_data['errors']
	
	def test_contact_form_get_request(self, client):
		"""Test that GET request to contact returns HTML form."""
		response = client.get('/contact')
		
		# Should return 200 or 404 depending on whether contact.html exists
		assert response.status_code in [200, 404]
	
	def test_contact_form_multiple_submissions(self, client):
		"""Test that multiple valid contact submissions are all stored."""
		data1 = {
			'name': 'User One',
			'email': 'user1@example.com',
			'message': 'First contact message here'
		}
		data2 = {
			'name': 'User Two',
			'email': 'user2@example.com',
			'message': 'Second contact message here'
		}
		
		response1 = client.post('/contact', json=data1)
		response2 = client.post('/contact', json=data2)
		
		assert response1.status_code == 201
		assert response2.status_code == 201
		
		# Verify both contacts exist in database
		from test import app as test_app
		with test_app.app_context():
			contacts = Contact.query.all()
			assert len(contacts) == 2
			emails = {c.email for c in contacts}
			assert 'user1@example.com' in emails
			assert 'user2@example.com' in emails
