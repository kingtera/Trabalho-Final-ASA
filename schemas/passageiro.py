from pydantic import BaseModel

class Passageiro(BaseModel):
    username: str
    nome_user: str
    email_user: str
    senha: str
    status: int