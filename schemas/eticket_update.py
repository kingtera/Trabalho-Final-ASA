from pydantic import BaseModel

class TicketUpdate(BaseModel):
    n_passagens: int