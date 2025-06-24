import os
from typing import Tuple

def validate_file_path(file_path: str) -> Tuple[bool, str]:
    """Check if file exists and is accessible"""
    if not os.path.exists(file_path):
        return False, "File does not exist"
    if not os.access(file_path, os.R_OK):
        return False, "File is not readable"
    return True, ""

def read_file_bytes(file_path: str) -> bytes:
    """Read file as binary data"""
    with open(file_path, 'rb') as f:
        return f.read()

def write_file_bytes(file_path: str, data: bytes) -> None:
    """Write binary data to file"""
    with open(file_path, 'wb') as f:
        f.write(data)

def get_output_filename(input_path: str, suffix: str = "_encrypted") -> str:
    """Generate output filename with suffix"""
    base, ext = os.path.splitext(input_path)
    return f"{base}{suffix}{ext}"