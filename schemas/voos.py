from pydantic import BaseModel
#from datetime import datetime

class Voo(BaseModel):
    #data_hora_voo: datetime
    #horario_voo: str
    #origem: int
    #destino: int
    #companhia:str
    #tarifa: str
    vagas: int