import getpass
from typing import Optional
from ..core import AESCipher
from ..utils.file_io import (
    read_file_bytes,
    write_file_bytes,
    validate_file_path,
    get_output_filename
)

class EncryptionCLI:
    def __init__(self):
        self.cipher = AESCipher()

    def get_password(self, confirm: bool = False) -> str:
        """Securely get password from user with optional confirmation"""
        while True:
            password = getpass.getpass("Enter password: ")
            if not confirm:
                return password
            
            confirm_pwd = getpass.getpass("Confirm password: ")
            if password == confirm_pwd:
                return password
            print("Passwords don't match. Try again.")

    def encrypt_file(self, input_path: str, output_path: Optional[str] = None) -> bool:
        """Handle file encryption process"""
        valid, msg = validate_file_path(input_path)
        if not valid:
            print(f"Error: {msg}")
            return False

        password = self.get_password(confirm=True)
        output_path = output_path or get_output_filename(input_path)

        try:
            plaintext = read_file_bytes(input_path)
            ciphertext = self.cipher.encrypt(plaintext, password)
            write_file_bytes(output_path, ciphertext)
            print(f"File encrypted successfully: {output_path}")
            return True
        except Exception as e:
            print(f"Encryption failed: {str(e)}")
            return False

    def decrypt_file(self, input_path: str, output_path: Optional[str] = None) -> bool:
        """Handle file decryption process"""
        valid, msg = validate_file_path(input_path)
        if not valid:
            print(f"Error: {msg}")
            return False

        password = self.get_password()
        output_path = output_path or get_output_filename(input_path, "_decrypted")

        try:
            ciphertext = read_file_bytes(input_path)
            plaintext = self.cipher.decrypt(ciphertext, password)
            write_file_bytes(output_path, plaintext)
            print(f"File decrypted successfully: {output_path}")
            return True
        except Exception as e:
            print(f"Decryption failed: {str(e)}")
            print("Possible causes: Incorrect password or corrupted file.")
            return False