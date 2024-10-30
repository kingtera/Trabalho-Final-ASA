from sqlalchemy import String, Integer, Float, Column, TIMESTAMP, text, ForeignKey, DATE
from database import Base

class Tickets(Base):
    __tablename__='ticket'

    id_ticket = Column(Integer, primary_key = True, autoincrement = True)
    voo = Column(Integer, ForeignKey('voos.id_voo'))
    n_passagens = Column(Integer)
    usr_comprador = Column(Integer, ForeignKey('users.id'))
    cod_reserva = Column(String(50), nullable=False)