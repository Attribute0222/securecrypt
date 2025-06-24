from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import hashlib

class KeyManager:
    def __init__(self, salt_size: int = 16, iterations: int = 100000):
        self.salt_size = salt_size
        self.iterations = iterations
    
    def generate_salt(self) -> bytes:
        """Generate cryptographically secure salt"""
        return get_random_bytes(self.salt_size)
    
    def derive_key(self, password: str, salt: bytes) -> bytes:
        """
        Derive encryption key using PBKDF2-HMAC-SHA256
        Args:
            password: User-provided password
            salt: Random salt value
        Returns:
            256-bit encryption key
        """
        return PBKDF2(
            password.encode('utf-8'),
            salt,
            dkLen=32,  # 256-bit key
            count=self.iterations,
            hmac_hash_module=hashlib.sha256
        )
    
    def verify_password_strength(self, password: str) -> bool:
        """Check if password meets minimum requirements"""
        return (
            len(password) >= 8
            and any(c.isupper() for c in password)
            and any(c.islower() for c in password)
            and any(c.isdigit() for c in password)
        )