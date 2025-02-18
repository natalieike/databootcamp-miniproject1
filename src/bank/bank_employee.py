'''Module for bank employee operations'''

from sqlalchemy import select
from src.bank.bank_schema import Employee
from src.utils.db import get_db
from src.utils.errors import log_error


class BankEmployee:
    '''Class for bank employee operations'''

    def __init__(self, employee_id, first_name, last_name, email, is_manager, department):
        if employee_id is not None:
            self.id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_manager = is_manager
        self.department = department

    def add_new(self):
        '''Saves the employee to the database'''
        new_employee = Employee(first_name=self.first_name, last_name=self.last_name,
                                email=self.email, is_manager=self.is_manager, department=self.department)

        with get_db() as db:
            try:
                db.add(new_employee)
            except Exception:
                log_error('Error saving employee')
                db.rollback()
            else:
                db.commit()
                db.refresh(new_employee)
        return new_employee

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
