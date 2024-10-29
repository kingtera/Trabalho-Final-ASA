from sqlalchemy import String, Integer, DateTime, Column, TIMESTAMP, text, ForeignKey, DATE
from .database import Base

class Voos(Base):
    __tablename__='voos'

    id_voo = Column(Integer, primary_key=True, autoincrement=True)
    data_hora_voo = Column(DateTime(timezone=True), nullable=False)
    #horario_voo = Column(TIMESTAMP(timezone=True), nullable=False)
    origem = Column(Integer, ForeignKey('aeroportos.id_aeroporto'))
    destino = Column(Integer, ForeignKey('aeroportos.id_aeroporto'))
    #companhia = Column(String(50), ForeignKey('companhias.nome'))
    tarifa = Column(String(50))
    vagas = Column(Integer, server_default = "0")
