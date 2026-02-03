from pydantic import BaseModel, ConfigDict, EmailStr, conint
from datetime import datetime
from typing import Optional

#USER CLASS
class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserOp(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str] = None

#POST CLASS
class Post(BaseModel):
    title: str
    content: str
    published: bool = True  #optional field(default true)

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    # title: str
    # content: str
    # published: bool
    created_at: datetime
    owner_id: int 
    owner:UserOp

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post : Post
    Votes : int
    
    class Config:
        orm_mode = True

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
    
    