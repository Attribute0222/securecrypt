import pytest
from click.testing import CliRunner
from encrypt_tool.cli.main import cli
import os

class TestCLI:
    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_encrypt_decrypt_flow(self, runner, tmp_path):
        # Create test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        # Test encryption
        result = runner.invoke(cli, ['encrypt', str(test_file)], input="password\npassword\n")
        assert result.exit_code == 0
        assert "encrypted successfully" in result.output
        
        # Test decryption
        encrypted = tmp_path / "test_encrypted.txt"
        result = runner.invoke(cli, ['decrypt', str(encrypted)], input="password\n")
        assert result.exit_code == 0
        assert "decrypted successfully" in result.output