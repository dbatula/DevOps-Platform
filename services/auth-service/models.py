from sqlalchemy import Column, Integer, String # type: ignore
from sqlalchemy.orm import declarative_base # type: ignore

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "auth_users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)