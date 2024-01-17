from sqlalchemy import Boolean, Column, Integer, String, func, Date, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone = Column(String(25))
    birthday = Column(Date)
    created_at = Column('created_at', DateTime, default=func.now())

