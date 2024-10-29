from fastapi import FastAPI
from models.user import Base
from routers.login import router as login_route
from routers.voos import router as voos_route
from routers.eticket import router as eticket_route
from database_login import engine


Base.metadata.create_all(bind=engine);

app = FastAPI();

app.include_router(login_route);
app.include_router(voos_route);
app.include_router(eticket_route);