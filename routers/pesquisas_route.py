from fastapi                        import FastAPI, HTTPException
from database_login                 import get_db
from datetime                       import date
from fastapi                        import APIRouter, Depends, HTTPException, Response, status
from fastapi.security               import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic                       import BaseModel
from typing                         import List
from sqlalchemy                     import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative     import declarative_base
from sqlalchemy.orm                 import sessionmaker, Session

router = APIRouter()


class Aeroporto(BaseModel):
    id_aeroporto: int
    nome: str
    cidade: str
    
class Voos(BaseModel):
    id_voo: int
    data_voo: date
    origem: str
    destino: str
    companhia: str
    tarifa: float
    vagas: int

@router.get("/aeroportos", response_model=List[Aeroporto])
def retornar_aeroportos(db: Session = Depends(get_db)):
    aeroportos = db.query(tb_aeroportos).all() #query(nome_da_tabela).all()
    return aeroportos

@router.get("/aeroportos/origem", response_model=List[Aeroporto])
def retornar_aeroportos_por_origem(cidade: str, db: Session = Depends(get_db)):
    # Consulta ao banco de dados filtrando pela cidade
    aeroportos = db.query(tb_aeroportos).filter(tb_aeroportos.cidade == cidade).all()
    
    # Verifica se nenhum aeroporto foi encontrado
    if not aeroportos:
        raise HTTPException(status_code=404, detail="Nenhum aeroporto encontrado para a cidade fornecida")
    
    return aeroportos


#retorna lista de voos oferecidos pela companhia na data informada
@router.get("/voos/data", response_model=List[Voos])
def retornar_voos_por_data(data: date, db: Session = Depends(get_db)):
    voos_data= db.query(tb_voos).filter(tb_voos.data == data).all()
    
    # Verifica se nenhum voo foi encontrado
    if not voos_data:
        raise HTTPException(status_code=404, detail="Nenhum voo encontrado para os dados fornecidos")
    
    return voos_data

@router.get("/pesquisar_voos", response_model=List[Voos])
def pesquisar_voos(origem: str, destino: str, passageiros: int, db: Session = Depends(get_db)):
    # Consulta ao banco de dados para encontrar voos que correspondem à origem e destino
    voos = db.query(tb_voos).filter(tb_voos.origem == origem, tb_voos.destino == destino).all()
    
    # Verifica se não encontrou voos
    if not voos:
        raise HTTPException(status_code=404, detail="Nenhum voo disponível com origem e destino informado")
    
    # Filtra voos que têm vagas suficientes
    voos_com_vagas = [voo for voo in voos if voo.vagas >= passageiros]
    
    # Verifica se há voos disponíveis com vagas suficientes
    if not voos_com_vagas:
        raise HTTPException(status_code=404, detail="Nenhum voo disponível com vagas suficientes")
    
    # Ordena os voos pelo valor da tarifa do menor para o maior
    voos_com_vagas.sort(key=lambda voo: voo.tarifa)

    return voos_com_vagas