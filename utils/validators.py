import re

def validate_email(email):
    """Validate email format."""
    if not email or not email.strip():
        return False, "Email cannot be empty"
    
    email = email.strip()
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Please enter a valid email address"
    
    return True, ""

def validate_phone(phone):
    """Validate phone number format."""
    if phone is None or phone.strip() == "":
        return True, ""  # Phone is optional
    
    # Remove spaces, hyphens, and parentheses
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    
    if not cleaned.isdigit():
        return False, "Phone number should contain only digits"
    
    if len(cleaned) < 10 or len(cleaned) > 15:
        return False, "Phone number should be between 10-15 digits"
    
    return True, ""

def validate_isbn(isbn):
    """Validate ISBN format."""
    if not isbn or not isbn.strip():
        return False, "ISBN cannot be empty"
    
    # Remove hyphens and spaces
    cleaned = isbn.replace("-", "").replace(" ", "")
    
    if not cleaned.isdigit():
        return False, "ISBN should contain only digits and hyphens"
    
    if len(cleaned) not in [10, 13]:
        return False, "ISBN should be 10 or 13 digits long"
    
    return True, ""

def validate_name(name, field_name="Name"):
    """Validate name fields."""
    if not name or not name.strip():
        return False, f"{field_name} cannot be empty"
    
    if len(name.strip()) < 2:
        return False, f"{field_name} must be at least 2 characters long"
    
    return True, ""

def get_valid_input(prompt, validator_func, field_name="Input"):
    """Get valid input from user with validation."""
    while True:
        user_input = input(prompt).strip()
        
        if user_input.lower() == 'q':
            return None  # User wants to quit
        
        is_valid, error_msg = validator_func(user_input)
        
        if is_valid:
            return user_input
        else:
            print(f"Error: {error_msg}")
            print("Please try again (or 'q' to go back)")

def get_yes_no_input(prompt):
    """Get yes/no input from user."""
    while True:
        response = input(f"{prompt} (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no")

def get_integer_input(prompt, min_val=None, max_val=None):
    """Get valid integer input from user."""
    while True:
        try:
            user_input = input(prompt).strip()
            
            if user_input.lower() == 'q':
                return None
            
            value = int(user_input)
            
            if min_val is not None and value < min_val:
                print(f"Please enter a number >= {min_val}")
                continue
            
            if max_val is not None and value > max_val:
                print(f"Please enter a number <= {max_val}")
                continue
            
            return value
            
        except ValueError:
            print("Please enter a valid number (or 'q' to go back)")

def get_menu_choice(prompt, min_choice, max_choice):
    """Get valid menu choice from user."""
    return get_integer_input(prompt, min_choice, max_choice)