'''Module for bank customer operations'''

from sqlalchemy import select
from src.bank.bank_schema import Customer
from src.utils.db import get_db
from src.utils.errors import log_error


class BankCustomer:
    '''Class for bank customer operations'''

    def __init__(self, customer_id, first_name, last_name, email, street_address, city, state, zip_code):
        if customer_id is not None:
            self.id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def add_new(self):
        '''Saves the customer to the database'''
        new_customer = Customer(first_name=self.first_name, last_name=self.last_name, email=self.email,
                                street_address=self.street_address, city=self.city, state=self.state, zip_code=self.zip_code)
        with get_db() as db:
            try:
                db.add(new_customer)
            except Exception:
                log_error('Error saving customer')
                db.rollback()
            else:
                db.commit()
                db.refresh(new_customer)
        return new_customer

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
