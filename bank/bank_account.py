'''Module for bank account operations'''

from bank_schema import Account
from sqlalchemy import select
from db import get_db
from errors import log_error


class BankAccount:
    '''Class for bank account operations'''

    def __init__(self, id, customer_id, account_type, balance, can_overdraft):
        self.id = id
        self.customer_id = customer_id
        self.type = account_type
        self.balance = balance
        self.can_overdraft = can_overdraft

    def save(self):
        '''Saves the account to the database'''
        with get_db() as db:
            try:
                db.add(self)
            except Exception:
                log_error('Error saving account')
                db.rollback()
            else:
                db.commit()
                db.refresh(self)

    @staticmethod
    def get_all():
        '''Returns all accounts from the database'''
        with get_db() as db:
            statement = select(Account)
            return db.scalars(statement).all()

    @staticmethod
    def get_all_by_customer_id(customer_id):
        '''Returns all accounts for a customer'''
        with get_db() as db:
            statement = select(Account).filter_by(customer_id=customer_id)
            return db.scalars(statement).all()

    @staticmethod
    def get_by_id(account_id):
        '''Returns an account by ID'''
        with get_db() as db:
            statement = select(Account).filter_by(id=account_id)
            return db.scalars(statement).first()

    def get_balance(self):
        '''Returns the balance of the account'''
        return self.balance

    def make_deposit(self, amount):
        '''Deposits money into the account'''
        self.balance += amount
        self.save()

    def make_withdrawal(self, amount):
        '''Withdraws money from the account'''
        if self.balance - amount < 0 and not self.can_overdraft:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.save()

    def set_balance(self, amount):
        '''Sets the balance of the account'''
        self.balance = amount
        self.save()

    def set_can_overdraft(self, can_overdraft):
        '''Sets the overdraft status of the account'''
        self.can_overdraft = can_overdraft
        self.save()

    def __repr__(self):
        return f"<BankAccount {self.type} for customer ID {self.customer_id}>"
