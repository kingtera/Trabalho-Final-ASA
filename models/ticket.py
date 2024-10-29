from sqlalchemy import String, Integer, Float, Column, TIMESTAMP, text, ForeignKey, DATE
from .database import Base

class Tickets(Base):
    __tablename__='ticket'

    id_ticket = Column(Integer, primary_key = True, autoincrement = True)
    voo = Column(Integer, ForeignKey('voos.id_voo'))
    passageiro = Column(Integer, ForeignKey('passageiro.id_user'))
    cod_reserva = Column(Integer, autoincrement = True)