from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os

class AESCipher:
    def __init__(self):
        self.salt_size = 16  # 128-bit salt
        self.key_size = 32   # 256-bit key
        self.iv_size = 16    # 128-bit IV
        self.iterations = 100000  # PBKDF2 iterations

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """Derive encryption key from password using PBKDF2"""
        return PBKDF2(password.encode(), salt, dkLen=self.key_size, count=self.iterations)

    def encrypt(self, plaintext: bytes, password: str) -> bytes:
        """Encrypt data with AES-256 CBC mode"""
        salt = get_random_bytes(self.salt_size)
        iv = get_random_bytes(self.iv_size)
        key = self._derive_key(password, salt)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
        return salt + iv + ciphertext

    def decrypt(self, ciphertext: bytes, password: str) -> bytes:
        """Decrypt AES-256 CBC encrypted data"""
        salt = ciphertext[:self.salt_size]
        iv = ciphertext[self.salt_size:self.salt_size+self.iv_size]
        encrypted_data = ciphertext[self.salt_size+self.iv_size:]
        key = self._derive_key(password, salt)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(encrypted_data), AES.block_size)