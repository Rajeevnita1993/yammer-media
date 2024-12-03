from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    phone_number: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    phone_number: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime 
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class DirectionEnum(int, Enum):
    ZERO = 0
    ONE = 1

class Vote(BaseModel):
    post_id: int
    dir: DirectionEnum


