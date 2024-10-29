from fastapi import FastAPI
from typing import Optional
from routers.aeroportos import router as router_aeroportos
from models.user import Base
from routers.login import router as login_route
from routers.voos import router as voos_route
from routers.eticket import router as eticket_route
from database_login import engine
#from routers.comp_aeroportos import router as router_comp_aeroportos
from routers.passageiro import router as router_passageiro
from routers.ticket import router as router_ticket
from routers.voos import router as router_voos
from models.database import engine
from models.aeroportos import Aeroportos
from models.aeroportos import Base
from models.passageiro import Passageiros
from models.passageiro import Base
from models.ticket import Tickets
from models.ticket import Base
from models.voos import Voos
from models.voos import Voos

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router_aeroportos)
#app.include_router(router_comp_aeroportos)
app.include_router(router_passageiro)
app.include_router(router_ticket)
app.include_router(router_voos)



Base.metadata.create_all(bind=engine);

app = FastAPI();

app.include_router(login_route);
app.include_router(voos_route);
app.include_router(eticket_route);