from fastapi          import APIRouter, Depends, HTTPException, Response, status
from schemas.ticket   import Ticket
from models.database  import get_db
from models.ticket    import Tickets
from sqlalchemy.orm   import Session
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

@router.get("/tickets")
def get(db: Session = Depends(get_db)):
    all_Tickets = db.query(Tickets).all()
    return all_Tickets


@router.post("/tickets")
async def criar_tickets(Ticket: Ticket, db: Session = Depends(get_db)):
    novo_Ticket = Tickets(**Ticket.model_dump())
    try:
        db.add(novo_Ticket)
        db.commit()
        db.refresh(novo_Ticket)
        return { "mensagem": "Ticket criado com sucesso",
                 "novo_Ticket": novo_Ticket}
    except Exception as e:
            print(e)
            return { "mensagem": "Problemas para gerar o Ticket",
                 "novo_Ticket": novo_Ticket}
    


@router.delete("/tickets/{id}")
def delete(id:int ,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT):
    delete_post = db.query(Tickets).filter(Tickets.id_ticket == id)
    
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ticket não existe")
    else:
        delete_post.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)   


@router.put("/tickets/{id}")
def update(id: int, Ticket:Ticket, db:Session = Depends(get_db)):
    updated_post = db.query(Tickets).filter(Tickets.id_ticket == id)
    updated_post.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Ticket: {id} does not exist')
    else:
        updated_post.update(Curso.model_dump(), synchronize_session=False)
        db.commit()
    return updated_post.first()