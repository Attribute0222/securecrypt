import os
import re

def validate_password(password: str) -> tuple:
    """Check password meets complexity requirements"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain uppercase letters"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain lowercase letters"
    if not re.search(r"[0-9]", password):
        return False, "Password must contain numbers"
    return True, ""

def validate_output_path(path: str) -> bool:
    """Check if output path is writable"""
    dirname = os.path.dirname(path) or '.'
    return os.access(dirname, os.W_OK)