from sqlalchemy import String, Integer, Column
from database import Base

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    full_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    status = Column(Integer, nullable=False)
    hashed_password = Column(String(100), nullable=False)