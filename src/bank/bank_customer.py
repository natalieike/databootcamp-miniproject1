'''Module for bank customer operations'''

from sqlalchemy import select
from bank.bank_schema import Customer
from utils.db import get_db
from utils.errors import log_error


class BankCustomer:
    '''Class for bank customer operations'''

    def __init__(self, customer_id, first_name, last_name, email, street_address, city, state, zip_code):
        self.id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def save(self):
        '''Saves the customer to the database'''
        with get_db() as db:
            try:
                db.add(self)
            except Exception:
                log_error('Error saving customer')
                db.rollback()
            else:
                db.commit()
                db.refresh(self)

    @staticmethod
    def get_all():
        '''Returns all customers from the database'''
        with get_db() as db:
            statement = select(Customer)
            return db.scalars(statement).all()

    @staticmethod
    def get_by_id(customer_id):
        '''Returns a customer by ID'''
        with get_db() as db:
            statement = select(Customer).filter_by(id=customer_id)
            return db.scalars(statement).first()

    def __repr__(self):
        return f"<BankCustomer {self.first_name} {self.last_name}>"
