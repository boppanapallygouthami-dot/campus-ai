import re
import validators

def validate_email(email: str) -> bool:
    """Validate email format using the validators package."""
    return bool(validators.email(email))

def validate_password(password: str) -> bool:
    """
    Validate that password meets strength guidelines:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    """
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

def validate_mobile(mobile: str) -> bool:
    """Validate mobile number (exactly 10 digits)."""
    return bool(re.match(r"^\d{10}$", mobile))

def validate_student_id(student_id: str) -> bool:
    """Validate student ID format (e.g. STU followed by digits or alphanumeric, not empty)."""
    if not student_id:
        return False
    return bool(re.match(r"^[A-Z0-9-]{3,15}$", student_id.upper()))
