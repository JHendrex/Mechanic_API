from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from typing import List

#Create base class for models
class Base(DeclarativeBase):
    pass

#Instantiate SQLAlchemy database

db = SQLAlchemy(model_class = Base)


class Customers(Base):
    __tablename__ = 'customers'
    
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(db.String(255), nullable=False)
    email:Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String(360), nullable=False)
    phone:Mapped[str] = mapped_column(db.String(15), nullable=False, unique=True)
    
    service_tickets:Mapped[List['Service_Tickets']] = db.relationship(back_populates='customer')
    
service_mechanics = db.Table(
    'service_mechanics',
    Base.metadata,
    db.Column('ticket_id', db.ForeignKey('service_tickets.id')),
    db.Column('mechanic_id', db.ForeignKey('mechanics.id'))
)

class Service_Tickets(Base):
    __tablename__ = 'service_tickets'
    
    id:Mapped[int] = mapped_column(primary_key=True)
    VIN:Mapped[str] = mapped_column(db.String(17), nullable=False)
    service_date: Mapped[date] = mapped_column(db.Date)
    service_desc:Mapped[str] = mapped_column(db.String(255), nullable=False)
    customer_id:Mapped[int] = mapped_column(db.ForeignKey('customers.id'))
    
    customer:Mapped['Customers'] = db.relationship(back_populates='service_tickets')
    mechanics:Mapped[List['Mechanics']] = db.relationship(secondary=service_mechanics, back_populates='service_tickets')
    
class Mechanics(Base):
    __tablename__ = 'mechanics'
    
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(db.String(255), nullable=False)
    email:Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone:Mapped[str] = mapped_column(db.String(15), nullable=False, unique=True)
    salary:Mapped[float] = mapped_column(db.Float, nullable=False)
    
    service_tickets:Mapped[list['Service_Tickets']] = db.relationship(secondary=service_mechanics, back_populates='mechanics')