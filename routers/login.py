from typing               import Annotated
from fastapi              import APIRouter, Depends, HTTPException, Response, status
from fastapi.security     import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing               import Annotated
from database       import get_db
from models.user          import Users
from schemas.user  import User
from sqlalchemy.orm       import Session
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone
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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = get_user(username, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuario não existe")
    
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(token_data.username, db)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.status:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

#CRUD USUARIOS
@router.get("/users")
def get(db: Session = Depends(get_db)):
    all_users = db.query(Users).all()
    logging.info("GET_ALL_USERS")
    users_list = []
    for user in all_users:
        item = {"id": user.id,
                "username": user.username}
        users_list.append(item)       
    logging.info(users_list)
    return all_users


@router.post("/users")
async def create_user(user: User, db: Session = Depends(get_db)):
    new_user = Users(**user.model_dump())
    try:
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logging.info("Usuario criado com sucesso")
        return { "mensagem": "usuario criado com sucesso",
                 "usuario": new_user}
    except Exception as e:
            logging.error(e)
            return { "mensagem": "Problemas para inserir o usuario",
                 "usuario": new_user}
    
@router.delete("/users/{id}")
def delete(id:int ,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT):
    delete_post = db.query(Users).filter(Users.id == id).first()
    
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuario não existe")
    else:
        delete_post.delete(synchronize_session=False)
        db.commit()
        logging.info("Usuario deletado com sucesso")

    return Response(status_code=status.HTTP_204_NO_CONTENT)   


@router.put("/users/{id}")
def update(id: int, user:User, db:Session = Depends(get_db)):
    updated_post = db.query(Users).filter(Users.id == id)
    updated_post.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Usuario: {id} does not exist')
    else:
        updated_post.update(user.model_dump(), synchronize_session=False)
        db.commit()
        logging.info("Usuario alterado com sucesso")

    return updated_post.first()

@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]