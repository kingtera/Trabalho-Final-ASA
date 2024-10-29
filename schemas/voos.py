from pydantic import BaseModel
<<<<<<< HEAD
#from datetime import datetime

class Voo(BaseModel):
    #data_hora_voo: datetime
    #horario_voo: str
    #origem: int
    #destino: int
    #companhia:str
    #tarifa: str
=======
from datetime import datetime

class Voo(BaseModel):
    data_hora_voo: datetime
    #horario_voo: str
    origem: int
    destino: int
    #companhia:str
    tarifa: str
>>>>>>> main
    vagas: int