from typing               import Annotated
from fastapi              import APIRouter, Depends, HTTPException, Response, status
from fastapi.security     import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing               import Annotated
from database_login       import get_db
from models.voos          import Voos
from schemas.voos  import Voo
from sqlalchemy.orm       import Session
import logging
from pydantic import BaseModel


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


#CRUD VOOS
@router.get("/voos")
def get(db: Session = Depends(get_db)):
    all_voos = db.query(Voos).all()
    logging.info("GET_ALL_voos")
    voos_list = []
    for voos in all_voos:
        item = {"id": voos.id_voo,
                "vagas": voos.vagas}
        voos_list.append(item)       
    logging.info(voos_list)
    return all_voos


@router.post("/voos")
async def create_eticket(voo: Voo, db: Session = Depends(get_db)):
    new_Voo = Voos(**voo.model_dump())
    try:
        
        db.add(new_Voo)
        db.commit()
        db.refresh(new_Voo)
        logging.info("Voo criado com sucesso")
        return { "mensagem": "Voo criado com sucesso",
                 "voo": new_Voo}
    except Exception as e:
            logging.error(e)
            return { "mensagem": "Problemas para inserir o new_Voo",
                 "voo": new_Voo}
    
@router.delete("/voos/{id}")
def delete(id:int ,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT):
    delete_post = db.query(Voos).filter(Voos.id_voo == id)
    
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Voo não existe")
    else:
        delete_post.delete(synchronize_session=False)
        db.commit()
        logging.info("Voo deletado com sucesso")

    return Response(status_code=status.HTTP_204_NO_CONTENT)   


@router.put("/voos/{id}")
def update(id: int, voo:Voo, db:Session = Depends(get_db)):
    updated_post = db.query(Voos).filter(Voos.id_voo == id)
    updated_post.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'voo: {id} does not exist')
    else:
        updated_post.update(voo.model_dump(), synchronize_session=False)
        db.commit()
        logging.info("voo alterado com sucesso")

    return updated_post.first()