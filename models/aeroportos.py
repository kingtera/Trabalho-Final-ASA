from sqlalchemy import String, Integer, Float, Column, TIMESTAMP, text, ForeignKey, DATE
from database import Base

class Aeroportos(Base):
    __tablename__='aeroportos'

    id_aeroporto =  Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable = False)
    cidade = Column(String(100), nullable = False)