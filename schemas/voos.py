from pydantic import BaseModel
from datetime import datetime

class Voo(BaseModel):
    data_hora_voo: datetime
    origem: int
    destino: int
    tarifa: str
    vagas: int