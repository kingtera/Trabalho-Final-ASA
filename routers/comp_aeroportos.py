# from fastapi          import APIRouter, Depends, HTTPException, Response, status
# from schemas.comp_aeroportos   import Comp_aeroportos
# from models.database  import get_db
# from models.comp_aeroportos    import Comp_aeroportos
# from sqlalchemy.orm   import Session
# import logging

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# router = APIRouter()

# @router.get("/comp_aeroportos")
# def get(db: Session = Depends(get_db)):
#     all_comp_aeroportos = db.query(Comp_aeroportos).all()
#     return all_comp_aeroportos