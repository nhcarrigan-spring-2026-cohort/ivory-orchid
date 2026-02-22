"""
Unit tests for validation functions.
Tests all validation logic in isolation.
"""
import pytest
from app.validators import (
    validate_required_field,
    validate_email,
    validate_age,
    validate_user_data,
    validate_contact_data
)


class TestValidateRequiredField:
    """Tests for validate_required_field function."""
    
    def test_valid_required_field(self):
        """Test that a non-empty string is valid."""
        is_valid, error = validate_required_field("John", "Name")
        assert is_valid is True
        assert error is None
    
    def test_empty_string_is_invalid(self):
        """Test that an empty string is invalid."""
        is_valid, error = validate_required_field("", "Name")
        assert is_valid is False
        assert "required" in error.lower()
    
    def test_whitespace_only_is_invalid(self):
        """Test that whitespace-only strings are invalid."""
        is_valid, error = validate_required_field("   ", "Name")
        assert is_valid is False
        assert "required" in error.lower()
    
    def test_none_is_invalid(self):
        """Test that None is invalid."""
        is_valid, error = validate_required_field(None, "Name")
        assert is_valid is False
        assert "required" in error.lower()


class TestValidateEmail:
    """Tests for validate_email function."""
    
    def test_valid_email(self):
        """Test that a valid email is accepted."""
        is_valid, error = validate_email("user@example.com")
        assert is_valid is True
        assert error is None
    
    def test_valid_email_with_subdomain(self):
        """Test that an email with subdomain is valid."""
        is_valid, error = validate_email("user@mail.example.co.uk")
        assert is_valid is True
        assert error is None
    
    def test_invalid_email_missing_at(self):
        """Test that email without @ is invalid."""
        is_valid, error = validate_email("userexample.com")
        assert is_valid is False
        assert "email" in error.lower()
    
    def test_invalid_email_missing_domain(self):
        """Test that email without domain is invalid."""
        is_valid, error = validate_email("user@")
        assert is_valid is False
        assert "email" in error.lower()
    
    def test_invalid_email_missing_local_part(self):
        """Test that email without local part is invalid."""
        is_valid, error = validate_email("@example.com")
        assert is_valid is False
        assert "email" in error.lower()
    
    def test_empty_email_is_invalid(self):
        """Test that empty email is invalid."""
        is_valid, error = validate_email("")
        assert is_valid is False
        assert "required" in error.lower()
    
    def test_none_email_is_invalid(self):
        """Test that None email is invalid."""
        is_valid, error = validate_email(None)
        assert is_valid is False
        assert "required" in error.lower()


class TestValidateAge:
    """Tests for validate_age function."""
    
    def test_valid_age_as_integer(self):
        """Test that a valid integer age is accepted."""
        is_valid, error = validate_age(25)
        assert is_valid is True
        assert error is None
    
    def test_valid_age_as_string(self):
        """Test that a valid age as string is converted and accepted."""
        is_valid, error = validate_age("30")
        assert is_valid is True
        assert error is None
    
    def test_age_one_is_valid(self):
        """Test that age 1 is minimum valid age."""
        is_valid, error = validate_age(1)
        assert is_valid is True
        assert error is None
    
    def test_age_zero_is_invalid(self):
        """Test that age 0 is invalid."""
        is_valid, error = validate_age(0)
        assert is_valid is False
        assert "positive" in error.lower()
    
    def test_negative_age_is_invalid(self):
        """Test that negative age is invalid."""
        is_valid, error = validate_age(-5)
        assert is_valid is False
        assert "positive" in error.lower()
    
    def test_age_over_150_is_invalid(self):
        """Test that unrealistic age (150+) is invalid."""
        is_valid, error = validate_age(151)
        assert is_valid is False
        assert "realistic" in error.lower()
    
    def test_age_150_is_valid(self):
        """Test that age 150 is acceptable."""
        is_valid, error = validate_age(150)
        assert is_valid is True
        assert error is None
    
    def test_non_numeric_age_is_invalid(self):
        """Test that non-numeric age is invalid."""
        is_valid, error = validate_age("abc")
        assert is_valid is False
        assert "integer" in error.lower()
    
    def test_float_age_as_string_is_invalid(self):
        """Test that float age string is invalid."""
        is_valid, error = validate_age("25.5")
        assert is_valid is False
        assert "integer" in error.lower()
    
    def test_none_age_is_invalid(self):
        """Test that None age is invalid."""
        is_valid, error = validate_age(None)
        assert is_valid is False
        assert "required" in error.lower()


class TestValidateUserData:
    """Tests for validate_user_data function."""
    
    def test_valid_user_data(self):
        """Test that valid user data passes validation."""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'age': 25
        }
        is_valid, errors = validate_user_data(data)
        assert is_valid is True
        assert errors == {}
    
    def test_missing_name(self):
        """Test that missing name causes validation error."""
        data = {
            'email': 'john@example.com',
            'age': 25
        }
        is_valid, errors = validate_user_data(data)
        assert is_valid is False
        assert 'name' in errors
    
    def test_missing_email(self):
        """Test that missing email causes validation error."""
        data = {
            'name': 'John Doe',
            'age': 25
        }
        is_valid, errors = validate_user_data(data)
        assert is_valid is False
        assert 'email' in errors
    
    def test_missing_age(self):
        """Test that missing age causes validation error."""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com'
        }
        is_valid, errors = validate_user_data(data)
        assert is_valid is False
        assert 'age' in errors
    
    def test_invalid_email_in_user_data(self):
        """Test that invalid email in user data causes error."""
        data = {
            'name': 'John Doe',
            'email': 'invalid-email',
            'age': 25
        }
        is_valid, errors = validate_user_data(data)
        assert is_valid is False
        assert 'email' in errors
    
    def test_invalid_age_in_user_data(self):
        """Test that invalid age in user data causes error."""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'age': -5
        }
        is_valid, errors = validate_user_data(data)
        assert is_valid is False
        assert 'age' in errors
    
    def test_short_name_is_invalid(self):
        """Test that name less than 2 characters is invalid."""
        data = {
            'name': 'J',
            'email': 'john@example.com',
            'age': 25
        }
        is_valid, errors = validate_user_data(data)
        assert is_valid is False
        assert 'name' in errors
    
    def test_very_long_name_is_invalid(self):
        """Test that name exceeding 120 characters is invalid."""
        data = {
            'name': 'A' * 121,
            'email': 'john@example.com',
            'age': 25
        }
        is_valid, errors = validate_user_data(data)
        assert is_valid is False
        assert 'name' in errors
    
    def test_multiple_errors_reported(self):
        """Test that multiple validation errors are reported."""
        data = {
            'name': 'J',
            'email': 'invalid-email',
            'age': -5
        }
        is_valid, errors = validate_user_data(data)
        assert is_valid is False
        assert 'name' in errors
        assert 'email' in errors
        assert 'age' in errors


class TestValidateContactData:
    """Tests for validate_contact_data function."""
    
    def test_valid_contact_data(self):
        """Test that valid contact data passes validation."""
        data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'message': 'This is a valid message'
        }
        is_valid, errors = validate_contact_data(data)
        assert is_valid is True
        assert errors == {}
    
    def test_missing_name(self):
        """Test that missing name causes validation error."""
        data = {
            'email': 'jane@example.com',
            'message': 'This is a valid message'
        }
        is_valid, errors = validate_contact_data(data)
        assert is_valid is False
        assert 'name' in errors
    
    def test_missing_email(self):
        """Test that missing email causes validation error."""
        data = {
            'name': 'Jane Doe',
            'message': 'This is a valid message'
        }
        is_valid, errors = validate_contact_data(data)
        assert is_valid is False
        assert 'email' in errors
    
    def test_missing_message(self):
        """Test that missing message causes validation error."""
        data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com'
        }
        is_valid, errors = validate_contact_data(data)
        assert is_valid is False
        assert 'message' in errors
    
    def test_message_too_short(self):
        """Test that message shorter than 10 characters is invalid."""
        data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'message': 'Too short'
        }
        is_valid, errors = validate_contact_data(data)
        assert is_valid is False
        assert 'message' in errors
    
    def test_message_too_long(self):
        """Test that message exceeding 5000 characters is invalid."""
        data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'message': 'A' * 5001
        }
        is_valid, errors = validate_contact_data(data)
        assert is_valid is False
        assert 'message' in errors
    
    def test_minimum_message_length(self):
        """Test that message with exactly 10 characters is valid."""
        data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'message': 'Exactly10c'
        }
        is_valid, errors = validate_contact_data(data)
        assert is_valid is True
        assert errors == {}
    
    def test_invalid_email_in_contact_data(self):
        """Test that invalid email in contact data causes error."""
        data = {
            'name': 'Jane Doe',
            'email': 'invalid-email',
            'message': 'This is a valid message'
        }
        is_valid, errors = validate_contact_data(data)
        assert is_valid is False
        assert 'email' in errors
