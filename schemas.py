from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime


class PostCreate(BaseModel):
    title: str
    content: str


class UsersOutPydantic(BaseModel):
    id: int
    email: EmailStr
    name: str

    class Config:
        from_attributes = True


class PostPydantic(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    created_at: datetime
    owner: UsersOutPydantic

    class Config:
        from_attributes = True


class UsersPydantic(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class UserSchemas(BaseModel):
    id: int
    email: EmailStr
    name: str

    class Config:
        from_attributes = True


class Like(BaseModel):
    post_id: int
    dir: conint(le=1)
