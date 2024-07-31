from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
# from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from database import Base

class GenderChoice(PyEnum):
    MALE = "male"
    FEMALE = "female"

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    year = Column(Integer, index=True)
    is_published = Column(Boolean, index=True)

class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    nickname = Column(String)
    stu_id = Column(String)
    dob = Column(Date, nullable=False)
    gender = Column(SQLAlchemyEnum(GenderChoice), nullable=False)
    
class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    menu_name = Column(String)
    img_url = Column(String)
    price = Column(Integer)
    rating = Column(Integer)

    orders = relationship("Order", back_populates="menu", cascade="all, delete-orphan")

class Order(Base):
    __tablename__ = "ordermenu"

    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey('menus.id'))
    count = Column(Integer)

    menu = relationship("Menu", back_populates="orders")
