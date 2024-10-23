from sqlalchemy import String, Integer, Float, Column, TIMESTAMP, text, ForeignKey, DATE
from .database import Base

class Voos(Base):
    __tablename__='voos'

    id_voo = Column(Integer, primary_key=True, autoincrement=True)
    # data_voo = Column(DATE, nullable=False) FOREIGN KEY?
    horario_voo = Column(TIMESTAMP(timezone=True), nullable=False)
    origem = Column(String(50), nullable=False)
    destino = Column(String(50), nullable=False)
    companhia = Column(String(50), nullable=False)
    tarifa = Column(Float)
    vagas = Column(Integer, server_default = "0")
