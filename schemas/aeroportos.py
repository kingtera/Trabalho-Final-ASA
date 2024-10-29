from pydantic import BaseModel

class Aeroporto(BaseModel):
    nome: str
    cidade: str