from fastapi import FastAPI
from models.user import Base
from routers.login_route import router as login_route
from database_login import engine


Base.metadata.create_all(bind=engine);

app = FastAPI();

app.include_router(login_route);