"""
Setup Module for Crossplane Examples.
"""
import setuptools

VERSION = '0.0.1'

setuptools.setup(
    name = 'crossplane_examples',
    version = VERSION,
    description = 'Crossplane Examples',
    long_description = open('README.md').read(),
    packages = setuptools.find_packages(),
    package_data = {
        'crossplane_examples': [
            '*',
        ],
    },
    install_requires = [
        'boto3',
        'flask',
        'flask_cors',
        'psycopg2',
        'psycopg2_binary',
    ],
    extras_require = {
        'test': [
            'pytest',
            'pytest-cov',
            'pylint',
        ]
    },
)
