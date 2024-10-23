from pydantic import BaseModel

class Companhias(BaseModel):
    id_companhia: int
    nome: str