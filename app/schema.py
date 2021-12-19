from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint
from sqlalchemy.sql.sqltypes import Integer
from typing import Optional

from app.database import Base

# setting a Schema for the posts

# Create different schemas for different kind of requests, in that way we can decide what the user will be able to do when in the different requests.
# PostBase and PostCreate handles data from user sending data to us


class PostBase(BaseModel):  # all PyDantic models needs to extend BaseModel
    title: str
    content: str
    published: bool = True

    # ratings: Optional[int] = None


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
# Post handles data sending data from us to user, specify what data should come back to the user.

# Since class Post inherit class PostBase it already have title, content and published. In this way we do not need do write that again.

# In class post we simply add owner_id and datatype and save. This will now return owner id because
# the schema of what we want to return to user says so.

# To get user information when retrieving a post, I added "owner" and called the schema "userOut".
# make sure the called for schema is above class Post for it to work.


class Post(PostBase):
    id: str
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:   # Tells pydantic that "we know it is not a dict, but convert it anyways"
        orm_mode = True


# Pydantic's orm_mode will tell Pydantic model to read the data even if it is not a dict, but an ORM model(or any other arbitrary object with attributes).

class UserCreate(BaseModel):
    # import from pydantic. Makes sure it is a valid email and not random text.
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # less than 1. Neg. accetps negative numbers
