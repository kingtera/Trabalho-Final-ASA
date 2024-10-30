from pydantic import BaseModel

class Ticket(BaseModel):
    voo: int
    n_passagens: int
    cod_reserva: int