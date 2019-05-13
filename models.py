from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Float, String, ForeignKey, Integer, DateTime
from settings import app
import datetime

db = SQLAlchemy(app)

# Class Company

class Company(db.Model):
    __tablename__ = "Company"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)


class CompanyProduct(db.Model):
    __tablename__ = "CompanyProduct"
    id = Column(String, primary_key=True)
    value = Column(Float, nullable=False)
    company = Column(String, ForeignKey('Company.id'))

class PhoneRecharge(db.Model):
    __tablename__ = "PhoneRecharge"
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    company_id = Column(String, ForeignKey('Company.id'))
    product_id = Column(String, ForeignKey('CompanyProduct.id'))
    phone_number = Column(String, nullable=False)
    value = Column(Float, nullable=False)



