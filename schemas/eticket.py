from pydantic import BaseModel

class Ticket(BaseModel):
    voo: int
    passageiro_titular: str
    numero_de_passageiros: int
    cod_reserva: int
    