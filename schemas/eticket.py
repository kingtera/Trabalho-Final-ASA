from pydantic import BaseModel

class Ticket(BaseModel):
    voo: int
    passageiro: int
    cod_reserva: int
    