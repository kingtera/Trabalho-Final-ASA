from sqlalchemy import String, Integer, Float, Column, TIMESTAMP, text, ForeignKey, DATE
from .database import Base

class Passageiro(Base):
    __tablename__='passageiro'

    id_user = Column(Integer, primary_key = True, auoincrement = True)
    nome_user = Column(String(100), nullable = False)
    idade_user = Column(Integer, nullable = False)