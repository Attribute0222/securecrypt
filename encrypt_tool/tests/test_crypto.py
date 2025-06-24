import os
import pytest
from ..core.crypto import AESCipher

class TestAESCipher:
    @pytest.fixture
    def cipher(self):
        return AESCipher()

    def test_encrypt_decrypt(self, cipher):
        test_data = b"Test secret data 123!"
        password = "securepassword123"
        
        # Test encryption and decryption
        encrypted = cipher.encrypt(test_data, password)
        decrypted = cipher.decrypt(encrypted, password)
        
        assert decrypted == test_data

    def test_wrong_password(self, cipher):
        test_data = b"Test data"
        encrypted = cipher.encrypt(test_data, "rightpassword")
        
        with pytest.raises(Exception):
            cipher.decrypt(encrypted, "wrongpassword")