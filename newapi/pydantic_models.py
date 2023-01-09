from pydantic import BaseModel
import uuid



class createuser(BaseModel):
    name : str
    email : str
    password :str
    phone : str

class loginuser(BaseModel):
    email : str
    password : str

class updateuser(BaseModel):
    id : int
    name : str
    email : str
    password :str
    phone :int

class deleteuser(BaseModel):
    user_email : str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"