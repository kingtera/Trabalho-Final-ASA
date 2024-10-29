from fastapi                        import HTTPException
from database                       import get_db
from datetime                       import date
from fastapi                        import APIRouter, Depends, HTTPException
from typing                         import List
from sqlalchemy.orm                 import Session
from sqlalchemy                     import cast, Date
from models.aeroportos              import Aeroportos
from models.voos                    import Voos
from schemas.aeroportos             import Aeroporto
from schemas.voos                   import Voo
from datetime                       import date

router = APIRouter()


@router.get("/aeroportos", response_model=List[Aeroporto])
def retornar_aeroportos(db: Session = Depends(get_db)):
    aeroportos = db.query(Aeroportos).all() #query(nome_da_tabela).all()
    return aeroportos

@router.get("/aeroportos/origem", response_model=List[Aeroporto])
def retornar_aeroportos_por_origem(cidade: str, db: Session = Depends(get_db)):
    aeroportos = db.query(Aeroportos).filter(Aeroportos.cidade == cidade).all()
    
    if not aeroportos:
        raise HTTPException(status_code=404, detail="Nenhum aeroporto encontrado para a cidade fornecida")
    
    return aeroportos


@router.get("/voos/data", response_model=List[Voo])
def retornar_voos_por_data(data: date, db: Session = Depends(get_db)):
    #data_aux = datetime.fromisoformat(Voos.data_hora_voo)
    voos = db.query(Voos).filter(cast(Voos.data_hora_voo, Date) == data).all()
    
    if not voos:
        raise HTTPException(status_code=404, detail="Nenhum voo encontrado para os dados fornecidos")
    
    return voos

@router.get("/pesquisar_voos", response_model=List[Voo])
def pesquisar_voos(origem: str, destino: str, passageiros: int, db: Session = Depends(get_db)):
    voos = db.query(Voos).filter(Voos.origem == origem, Voos.destino == destino).all()
    
    if not voos:
        raise HTTPException(status_code=404, detail="Nenhum voo disponível com origem e destino informado")
    
    voos_com_vagas = [voo for voo in voos if voo.vagas >= passageiros]
    
    if not voos_com_vagas:
        raise HTTPException(status_code=404, detail="Nenhum voo disponível com vagas suficientes")
    
    voos_com_vagas.sort(key=lambda voo: voo.tarifa)

    return voos_com_vagas