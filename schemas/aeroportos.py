from pydantic import BaseModel

class Aeroportos(BaseModel):
    id_aeroporto: int
    nome: str
    cidade: str