from pydantic import BaseModel

class Passageiro(BaseModel):
    id_user: int
    nome_user: str
    idade_user: int