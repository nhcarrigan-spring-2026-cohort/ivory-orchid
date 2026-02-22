"""
Validation functions for form data and API inputs.
Provides backend validation to ensure data integrity before database operations.

Why backend validation is necessary:
1. Security: Frontend validation can be bypassed by direct API calls or malicious requests
2. Consistency: Ensures all data meets requirements regardless of client type (web, mobile, etc.)
3. Data Integrity: Prevents invalid data from corrupting the database
4. Reliability: Provides consistent validation rules across all endpoints
"""
from email_validator import validate_email as check_email, EmailNotValidError


def validate_required_field(value, field_name):
    """
    Validate that a field is provided and not empty.
    
    Args:
        value: The field value to validate
        field_name (str): The name of the field (for error messages)
        
    Returns:
        tuple: (is_valid, error_message or None)
    """
    if value is None or (isinstance(value, str) and value.strip() == ''):
        return False, f"{field_name} is required and cannot be empty"
    return True, None


def validate_email(email_str):
    """
    Validate email format using email_validator library.
    Checks RFC 5322 compliance and basic format.
    
    Args:
        email_str (str): Email address to validate
        
    Returns:
        tuple: (is_valid, error_message or None)
    """
    if not email_str:
        return False, "Email is required"
    
    try:
        # This will validate format and normalize the email
        # check_deliverability=False skips DNS checks for testing/development
        valid_email = check_email(email_str, check_deliverability=False)
        return True, None
    except EmailNotValidError as e:
        return False, f"Invalid email format: {str(e)}"


def validate_age(age):
    """
    Validate that age is a positive integer.
    
    Args:
        age: The age value to validate (could be string, int, etc.)
        
    Returns:
        tuple: (is_valid, error_message or None)
    """
    if age is None:
        return False, "Age is required"
    
    # Try to convert to integer if it's a string
    try:
        age_int = int(age)
    except (ValueError, TypeError):
        return False, "Age must be a valid integer"
    
    # Validate age is positive and reasonable
    if age_int < 1:
        return False, "Age must be a positive integer"
    
    if age_int > 150:
        return False, "Age must be a realistic value (less than 150)"
    
    return True, None


def validate_user_data(data):
    """
    Validate user registration data.
    
    Args:
        data (dict): Dictionary containing 'name', 'email', and 'age' fields
        
    Returns:
        tuple: (is_valid, errors_dict)
            - is_valid (bool): True if all fields are valid
            - errors_dict (dict): Dictionary of field names to error messages
                                 Empty dict if is_valid is True
    """
    errors = {}
    
    # Validate name
    is_valid, error = validate_required_field(data.get('name'), 'Name')
    if not is_valid:
        errors['name'] = error
    else:
        # Additional name validation: check length
        name = data.get('name', '').strip()
        if len(name) < 2:
            errors['name'] = 'Name must be at least 2 characters long'
        elif len(name) > 120:
            errors['name'] = 'Name must not exceed 120 characters'
    
    # Validate email
    is_valid, error = validate_email(data.get('email'))
    if not is_valid:
        errors['email'] = error
    
    # Validate age
    is_valid, error = validate_age(data.get('age'))
    if not is_valid:
        errors['age'] = error
    
    return len(errors) == 0, errors


def validate_contact_data(data):
    """
    Validate contact form submission data.
    
    Args:
        data (dict): Dictionary containing 'name', 'email', and 'message' fields
        
    Returns:
        tuple: (is_valid, errors_dict)
            - is_valid (bool): True if all fields are valid
            - errors_dict (dict): Dictionary of field names to error messages
                                 Empty dict if is_valid is True
    """
    errors = {}
    
    # Validate name
    is_valid, error = validate_required_field(data.get('name'), 'Name')
    if not is_valid:
        errors['name'] = error
    else:
        name = data.get('name', '').strip()
        if len(name) < 2:
            errors['name'] = 'Name must be at least 2 characters long'
        elif len(name) > 120:
            errors['name'] = 'Name must not exceed 120 characters'
    
    # Validate email
    is_valid, error = validate_email(data.get('email'))
    if not is_valid:
        errors['email'] = error
    
    # Validate message
    is_valid, error = validate_required_field(data.get('message'), 'Message')
    if not is_valid:
        errors['message'] = error
    else:
        message = data.get('message', '').strip()
        if len(message) < 10:
            errors['message'] = 'Message must be at least 10 characters long'
        elif len(message) > 5000:
            errors['message'] = 'Message must not exceed 5000 characters'
    
    return len(errors) == 0, errors
