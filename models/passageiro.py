from sqlalchemy import String, Integer, Float, Column, TIMESTAMP, text, ForeignKey, DATE
from .database import Base

class Passageiros(Base):
    __tablename__='passageiro'

    id_user = Column(Integer, primary_key = True, autoincrement = True)
    username = Column(String(100), nullable = False)
    nome_user = Column(String(100), nullable = False)
    email_user = Column(String(100), nullable = False)
    senha = Column(String(100), nullable = False)
    status = Column(Integer)
