'''Module for bank employee operations'''

from bank_schema import Employee
from sqlalchemy import select
from db import get_db
from errors import log_error


class BankEmployee:
    '''Class for bank employee operations'''

    def __init__(self, first_name, last_name, email, is_manager, department):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_manager = is_manager
        self.department = department

    def save(self):
        '''Saves the employee to the database'''
        with get_db() as db:
            try:
                db.add(self)
            except Exception:
                log_error('Error saving employee')
                db.rollback()
            else:
                db.commit()

    @staticmethod
    def get_all():
        '''Returns all employees from the database'''
        with get_db() as db:
            statement = select(Employee)
            return db.scalars(statement).all()

    @staticmethod
    def get_by_id(employee_id):
        '''Returns an employee by ID'''
        with get_db() as db:
            statement = select(Employee).filter_by(id=employee_id)
            return db.scalars(statement).first()

    def __repr__(self):
        return f"<BankEmployee {self.first_name} {self.last_name}>"
