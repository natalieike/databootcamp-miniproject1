'''Module for bank product operations'''

from bank_schema import Product
from sqlalchemy import select
from db import get_db
from errors import log_error


class BankProduct:
    '''Class for bank account operations'''

    def __init__(self, id, customer_id, product_type, balance, min_payment):
        self.id = id
        self.customer_id = customer_id
        self.type = product_type
        self.balance = balance
        self.min_payment = min_payment

    def save(self):
        '''Saves the account to the database'''
        with get_db() as db:
            try:
                db.add(self)
            except Exception:
                log_error('Error saving product')
                db.rollback()
            else:
                db.commit()

    @staticmethod
    def get_all():
        '''Returns all accounts from the database'''
        with get_db() as db:
            statement = select(Product)
            return db.scalars(statement).all()

    @staticmethod
    def get_all_by_customer_id(customer_id):
        '''Returns all products for a customer'''
        with get_db() as db:
            statement = select(Product).filter_by(customer_id=customer_id)
            return db.scalars(statement).all()

    @staticmethod
    def get_by_id(product_id):
        '''Returns a product by ID'''
        with get_db() as db:
            statement = select(Product).filter_by(id=product_id)
            return db.scalars(statement).first()

    def get_balance(self):
        '''Returns the balance of the account'''
        return self.balance

    def make_credit(self, amount):
        '''Adds money to the product balance'''
        self.balance += amount
        self.save()

    def make_debit(self, amount):
        '''Removes money from the product balance'''
        self.balance -= amount
        self.save()

    def make_payment(self, amount):
        '''Lowers the product balance by the payment amount'''
        if self.min_payment > amount:
            raise ValueError("Payment amount is less than the minimum payment")
        if self.balance - amount < 0:
            raise ValueError(
                "Payment amount is greater than the balance - you are overpaying")
        self.balance -= amount
        self.save()

    def set_balance(self, amount):
        '''Sets the balance of the account'''
        self.balance = amount
        self.save()

    def set_min_payment(self, min_payment):
        '''Sets the minimum payment of the account'''
        self.min_payment = min_payment
        self.save()

    def __repr__(self):
        return f"<BankAccount {self.type} for customer ID {self.customer_id}>"
