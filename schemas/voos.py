from pydantic import BaseModel

class Voos(BaseModel):
    id_voo: int
    horario_voo: str
    origem: str
    destino: str
    comphania = str
    tarifa = float
    vagas = int