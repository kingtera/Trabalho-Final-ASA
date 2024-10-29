from pydantic             import BaseModel
from hash_password        import get_password_hash   #function for hash


class User(BaseModel):
    username: str
    full_name: str 
    email: str 
    status: int
    hashed_password: get_password_hash