import re

def validate_age(age: int) -> bool:
    # AC-013: 18 <= age < 99
    return 18 <= age < 99

def validate_password(password: str) -> bool:
    # AC-014: min 8 chars and at least 1 digit
    if len(password) < 8:
        return False
    if not re.search(r"\d", password):
        return False
    return True