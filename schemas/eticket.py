from pydantic import BaseModel

class Ticket(BaseModel):
    voo: int
    cod_reserva: int
    