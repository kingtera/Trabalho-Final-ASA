from sqlalchemy import String, Integer, Float, Column, TIMESTAMP, text, ForeignKey, DATE
from .database import Base

class Ticket(Base):
    __tablename__='ticket'

    id_ticket = Column(Integer, primary_key = True, autoincrement = True)
    # voo = Column(Integer) FOREIGN KEY de voos(id_voo)
    # passageiro = Column(Integer) FOREIGN KEY de Passageiro(id_user)
    cod_reserva = Column(Integer, autoincrement = True)