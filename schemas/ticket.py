from pydantic import BaseModel

class Ticket(BaseModel):
    id_ticket: int
    cod_reserva: int