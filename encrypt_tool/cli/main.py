import click
from .interface import EncryptionCLI

@click.group()
def cli():
    """Advanced Encryption Tool - CLI Interface"""
    pass

@cli.command()
@click.argument('input_file')
@click.option('--output', '-o', help='Output file path')
def encrypt(input_file, output):
    """Encrypt a file"""
    cli_handler = EncryptionCLI()
    cli_handler.encrypt_file(input_file, output)

@cli.command()
@click.argument('input_file')
@click.option('--output', '-o', help='Output file path')
def decrypt(input_file, output):
    """Decrypt a file"""
    cli_handler = EncryptionCLI()
    cli_handler.decrypt_file(input_file, output)

if __name__ == '__main__':
    cli()