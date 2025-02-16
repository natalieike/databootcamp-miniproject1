'''Defines all of the database models'''

from sqlalchemy import ForeignKey, String, Integer, Float, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class ModelBase(DeclarativeBase):
    '''Base class for all models'''
    pass


class Customer(ModelBase):
    '''Defines the customer model'''
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(255))
    street_address: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(50))
    state: Mapped[str] = mapped_column(String(50))
    zip_code: Mapped[str] = mapped_column(String(10))

    accounts: Mapped[list['Account']] = relationship(
        "Account", back_populates="customer", cascade="all, delete-orphan")
    products: Mapped[list['Product']] = relationship(
        "Product", back_populates="customer", cascade="all, delete-orphan")


class Employee(ModelBase):
    '''Defines the employee model'''
    __tablename__ = "employee"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(255))
    is_manager: Mapped[bool] = mapped_column(Boolean)
    department: Mapped[str] = mapped_column(String(50))


class Account(ModelBase):
    '''Defines bank account model'''
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    type: Mapped[str] = mapped_column(String(50))
    balance: Mapped[float] = mapped_column(Float)
    can_overdraft: Mapped[bool] = mapped_column(Boolean)

    customer: Mapped["Customer"] = relationship(
        "Customer", back_populates="accounts")


class Product(ModelBase):
    '''Defines product model'''
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    type: Mapped[str] = mapped_column(String(50))
    balance: Mapped[float] = mapped_column(Float)
    min_payment: Mapped[float] = mapped_column(Float)

    customer: Mapped['Customer'] = relationship(
        "Customer", back_populates="products")
