from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key = True)
    name = Column(String(250),nullable = False)

class MenuItem(Base):
    __tablename__= 'menu_item'
    id=Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    description = Column(String(250))
    price= Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer,primary_key=True)
    name = Column(String(250), nullable =False)

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer,primary_key=True)
    street = Column(String(80), nullable = False)
    zip = Column(String(5), nullable = False)
    employee_id = Column(Integer, ForeignKey('employee.id'))
    employee = relationship(Employee)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)