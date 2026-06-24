from sqlalchemy import Column, Integer, String # type: ignore
from sqlalchemy.orm import declarative_base # type: ignore

Base = declarative_base()


class OrderDB(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    product_name = Column(String)
    quantity = Column(Integer)
    status = Column(String)