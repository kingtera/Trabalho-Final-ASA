from typing               import Annotated
from fastapi              import APIRouter, Depends, HTTPException, Response, status
from fastapi.security     import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing               import Annotated
from database_login       import get_db
from models.user          import Users
from models.eticket          import Tickets
from schemas.user  import User
from schemas.eticket  import Ticket
from sqlalchemy.orm       import Session
import logging
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "294944e7bed93b5848acee683f699b3e3015d94a7971185ea457f408a5ab849b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


#CRUD ETICKETS
@router.get("/etickets")
def get(db: Session = Depends(get_db)):
    all_etickets = db.query(Tickets).all()
    logging.info("GET_ALL_ETICKETS")
    etickets_list = []
    for eticket in all_etickets:
        item = {"id": eticket.id_ticket,
                "username": eticket.passageiro}
        etickets_list.append(item)       
    logging.info(etickets_list)
    return all_etickets


@router.post("/eticket")
async def create_eticket(ticket: Ticket, db: Session = Depends(get_db)):
    new_ticket = Tickets(**ticket.model_dump())
    try:
        
        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)
        logging.info("Ticket criado com sucesso")
        return { "mensagem": "ticket criado com sucesso",
                 "ticket": new_ticket}
    except Exception as e:
            logging.error(e)
            return { "mensagem": "Problemas para inserir o ticket",
                 "ticket": new_ticket}
    
@router.delete("/etickets/{id}")
def delete(id:int ,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT):
    delete_post = db.query(Tickets).filter(Tickets.id_ticket == id)
    
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ticket não existe")
    else:
        delete_post.delete(synchronize_session=False)
        db.commit()
        logging.info("Ticket deletado com sucesso")

    return Response(status_code=status.HTTP_204_NO_CONTENT)   


@router.put("/etickets/{id}")
def update(id: int, ticket:Ticket, db:Session = Depends(get_db)):
    updated_post = db.query(Tickets).filter(Tickets.id_ticket == id)
    updated_post.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Ticket: {id} does not exist')
    else:
        updated_post.update(ticket.model_dump(), synchronize_session=False)
        db.commit()
        logging.info("Ticket alterado com sucesso")

    return updated_post.first()