'''Module for bank product operations'''

from sqlalchemy import select
from bank.bank_schema import Product
from utils.db import get_db
from utils.errors import log_error


class BankProduct:
    '''Class for bank product operations'''

    def __init__(self, product_id, customer_id, product_type, balance, min_payment):
        if product_id is not None:
            self.id = product_id
        self.customer_id = customer_id
        self.type = product_type
        self.balance = balance
        self.min_payment = min_payment

    def add_new(self):
        '''Saves the product to the database'''
        with get_db() as db:
            new_product = Product(customer_id=self.customer_id, type=self.type,
                                  balance=self.balance, min_payment=self.min_payment)
            try:
                db.add(new_product)
            except Exception:
                log_error('Error saving product')
                db.rollback()
            else:
                db.commit()
                db.refresh(new_product)
            return new_product

    def save_balance(self):
        '''Updates the product balance in the database'''
        with get_db() as db:
            try:
                statement = select(Product).filter_by(id=self.id)
                to_update = db.scalars(statement).first()
                to_update.balance = self.balance
            except Exception:
                log_error('Error saving product')
                db.rollback()
            else:
                db.commit()

    @staticmethod
    def get_all():
        '''Returns all products from the database'''
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

    @staticmethod
    def get_by_id_and_customer_id(product_id, customer_id):
        '''Returns a product by ID and customer ID'''
        with get_db() as db:
            statement = select(Product).filter_by(
                id=product_id, customer_id=customer_id)
            return db.scalars(statement).first()

    def get_balance(self):
        '''Returns the balance of the product'''
        return self.balance

    def make_credit(self, amount):
        '''Removes money from the product balance'''
        self.balance -= amount
        self.save_balance()

    def make_debit(self, amount):
        '''Adds money to the product balance'''
        self.balance += amount
        self.save_balance()

    def set_balance(self, amount):
        '''Sets the balance of the product'''
        self.balance = amount
        self.save_balance()

    def set_min_payment(self, min_payment):
        '''Sets the minimum payment of the product'''
        self.min_payment = min_payment
        with get_db() as db:
            try:
                statement = select(Product).filter_by(id=self.id)
                to_update = db.scalars(statement).first()
                to_update.min_payment = self.min_payment
            except Exception:
                log_error('Error saving product')
                db.rollback()
            else:
                db.commit()

    def __repr__(self):
        return f"<BankProduct {self.type} for customer ID {self.customer_id}>"
