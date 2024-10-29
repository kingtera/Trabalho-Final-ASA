from fastapi import FastAPI
from routers.aeroportos import router as router_aeroportos
from routers.login import router as route_login
from routers.eticket import router as router_eticket
from routers.pesquisas import router as router_pesquisas
from database import engine
from routers.voos import router as router_voos
from models.user import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router_aeroportos)
app.include_router(router_eticket)
app.include_router(router_voos)
app.include_router(route_login)
app.include_router(router_pesquisas);