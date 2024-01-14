from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

import datetime

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    kakao_id = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.now())

class PriceLog(Base):
    __tablename__ = "price_logs"
    id = Column(Integer, primary_key=True)
    price = Column(Integer)

    items = relationship("Product", back_populates="price_logs")
    created_at = Column(DateTime, default=datetime.datetime.now())


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    
