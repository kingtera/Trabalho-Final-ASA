from pydantic import BaseModel

class User(BaseModel):
    username: str
    full_name: str 
    email: str 
    status: int

class UserInDB(User):
    hashed_password: str