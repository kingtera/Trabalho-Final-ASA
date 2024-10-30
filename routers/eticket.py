from typing               import Annotated
from fastapi              import APIRouter, Depends, HTTPException, Response, status
from fastapi.security     import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing               import Annotated
from database       import get_db
from models.voos          import Voos
from models.eticket          import Tickets
from schemas.user  import User
from schemas.eticket  import Ticket
from schemas.eticket_update import TicketUpdate
from sqlalchemy.orm       import Session
import logging
from pydantic import BaseModel
from .login import get_current_active_user

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
def get(current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    all_etickets = db.query(Tickets).filter(Tickets.usr_comprador == current_user.id)
    logging.info("GET_ALL_ETICKETS")
    etickets_list = []
    for eticket in all_etickets:
        item = {"id": eticket.id_ticket,
                "id_user": eticket.usr_comprador}
        etickets_list.append(item)       
    logging.info(etickets_list)
    return etickets_list


@router.post("/eticket")
async def create_eticket(current_user: Annotated[User, Depends(get_current_active_user)], ticket: Ticket, db: Session = Depends(get_db)):
    new_ticket = Tickets(
        voo=ticket.voo,
        n_passagens = ticket.n_passagens,
        usr_comprador=current_user.id,
        cod_reserva=ticket.cod_reserva
    )

    voo = db.query(Voos).filter(Voos.id_voo == new_ticket.voo).first()
    
    if voo.vagas < new_ticket.n_passagens:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Vagas insuficientes no voo para o número de passageiros solicitado. Restam {voo.vagas} passagen(s) restante(s) para esse voo"
        )
    else:
        voo.vagas = voo.vagas - new_ticket.n_passagens

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
def delete(current_user: Annotated[User, Depends(get_current_active_user)],id:int ,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT):
    delete_post = db.query(Tickets).filter(Tickets.id_ticket == id).first()
    
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ticket não existe")
    else:
        delete_post.delete(synchronize_session=False)
        db.commit()
        logging.info("Ticket deletado com sucesso")

    return Response(status_code=status.HTTP_204_NO_CONTENT)   


@router.put("/etickets/{id}")
def update_n_passagens(current_user: Annotated[User, Depends(get_current_active_user)],id: int, ticket:TicketUpdate, db:Session = Depends(get_db)):
    updated_post = db.query(Tickets).filter(Tickets.id_ticket == id)
    existing_ticket = updated_post.first()

    if existing_ticket == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Ticket: {id} does not exist')
    else:
        voo = db.query(Voos).filter(Voos.id_voo == existing_ticket.voo).first()
        dif = ticket.n_passagens - existing_ticket.n_passagens

        if dif > 0:
            if voo.vagas < dif:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Vagas insuficientes no voo para o número de passageiros solicitado. Restam {voo.vagas} passagen(s) restante(s) para esse voo"
                )
            else:
                voo.vagas = voo.vagas - dif
        elif dif < 0:
            voo.vagas = voo.vagas + (-dif)
        else:
            return {"msg":"Sem alteracao"}

        updated_post.update(ticket.model_dump(), synchronize_session=False)

        db.commit()
        logging.info("Ticket alterado com sucesso")

    return updated_post.first()