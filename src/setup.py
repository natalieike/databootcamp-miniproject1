'''setup.py'''

from setuptools import setup, find_packages

setup(
    name='bank',
    version='0.1.0',
    description='Simple bank application',
    author='Natalie Ike',
    packages=find_packages(
        include=['src', 'src.*', 'bank', 'bank.*', 'utils', 'utils.*']),
    install_requires=[
        'pytest==8.3.4',
        'python-dotenv==1.0.1',
        'SQLAlchemy==2.0.34'
    ],
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=['pytest'],
)
