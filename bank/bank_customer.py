'''Module for bank customer operations'''

from bank_db import get_db


def some_function():
    '''Performs database operations using the session'''
    with get_db() as db:
        # Perform database operations using the session 'db'
        result = db.execute("SELECT 1")
        print(result.scalar())
