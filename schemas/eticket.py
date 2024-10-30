from pydantic            import BaseModel
from gera_codigo_ticket  import gera_codigo_ticket 

class Ticket(BaseModel):
    voo: int
    n_passagens: int
    cod_reserva: gera_codigo_ticket