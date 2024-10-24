from pydantic import BaseModel
from datetime import date

class Voo(BaseModel):
    data_voo: date
    horario_voo: str
    origem: int
    destino: int
    #companhia:str
    tarifa: str
    vagas: int