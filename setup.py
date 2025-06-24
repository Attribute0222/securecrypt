from setuptools import setup, find_packages

setup(
    name="encryption_tool",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'pycryptodome>=3.9.0',
        'click>=7.0'
    ],
    entry_points={
        'console_scripts': [
            'encrypt-tool=encryption_tool.cli.main:cli'
        ]
    },
)