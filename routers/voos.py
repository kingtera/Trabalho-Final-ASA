from fastapi          import APIRouter, Depends, HTTPException, Response, status
from schemas.voos   import Voo
from database  import get_db
from models.voos    import Voos
from sqlalchemy.orm   import Session
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

@router.get("/voos")
def get(db: Session = Depends(get_db)):
    all_voos = db.query(Voos).all()
    logging.info("GET_ALL_VOOS")
    voos = []
    for voo in all_voos:
        item = {"id": voo.id_voo,
                "data": voo.data_hora_voo}
        voos.append(item)       
    logging.info(voos)
    return all_voos


@router.post("/voos")
async def criar_voos(voo: Voo, db: Session = Depends(get_db)):
    novo_voo = Voos(**voo.model_dump())
    try:
        db.add(novo_voo)
        db.commit()
        db.refresh(novo_voo)
        logging.info("Voo criado com sucesso")
        return { "mensagem": "Voo criado com sucesso",
                 "novo_voo": novo_voo}
    except Exception as e:
            logging.error(e)
            return { "mensagem": "Problemas para adicionar voo",
                 "novo_voo": novo_voo}

 
@router.delete("/voos/{id}")
def delete(id:int ,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT):
    delete_post = db.query(Voos).filter(Voos.id_voo == id).first()
    
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Voo não encontrado")
    else:
        delete_post.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)   


@router.put("/voos/{id}")
def update(id: int, voo: Voo, db:Session = Depends(get_db)):
    updated_post = db.query(Voos).filter(Voos.id_voo == id)
    updated_post.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Professor: {id} does not exist')
    else:
        updated_post.update(voo.model_dump(), synchronize_session=False)
        db.commit()
    return updated_post.first()