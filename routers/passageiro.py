from fastapi          import APIRouter, Depends, HTTPException, Response, status
from schemas.passageiro   import Passageiro
from models.database  import get_db
from models.passageiro    import Passageiros
from sqlalchemy.orm   import Session
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


router = APIRouter()

@router.get("/passageiros")
def get(db: Session = Depends(get_db)):
    all_passageiros = db.query(Passageiros).all()
    logging.info("GET_ALL_Passageiros")
    passageiros = []
    for passageiro in all_passageiros:
        item = {"id": passageiro.id_user,
                "nome": passageiro.nome_user}
        passageiros.append(item)       
    logging.info(passageiros)
    return all_passageiros


@router.post("/passageiros")
async def criar_passageiro(passageiro: Passageiro, db: Session = Depends(get_db)):
    novo_passageiro = Passageiros(**passageiro.model_dump())
    try:
        
        db.add(novo_passageiro)
        db.commit()
        db.refresh(novo_passageiro)
        logging.info("Usuário criado com sucesso")
        return { "mensagem": "Usuário criado com sucesso",
                 "passageiro": novo_passageiro}
    except Exception as e:
            logging.error(e)
            return { "mensagem": "Problemas para inserir o usuário",
                 "passageiro": novo_passageiro}
 
@router.delete("/passageiros/{id}")
def delete(id:int ,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT):
    delete_post = db.query(Passageiros).filter(Passageiros.id_user == id)
    
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuário não existe")
    else:
        delete_post.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)   


@router.put("/passageiros/{id}")
def update(id: int, passageiro:Passageiro, db:Session = Depends(get_db)):
    updated_post = db.query(Passageiros).filter(Passageiros.id_user == id)
    updated_post.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Passageiro: {id} does not exist')
    else:
        updated_post.update(passageiro.model_dump(), synchronize_session=False)
        db.commit()
    return updated_post.first()