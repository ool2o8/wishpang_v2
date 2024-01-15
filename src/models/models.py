from sqlalchemy import BIGINT, Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

import datetime

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(BIGINT, primary_key=True)
    kakao_id = Column(BIGINT, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.now())

class PriceLog(Base):
    __tablename__ = "price_logs"
    id = Column(Integer, primary_key=True)
    price = Column(BIGINT)
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", backref="price_logs")
    created_at = Column(DateTime, default=datetime.datetime.now())


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    
