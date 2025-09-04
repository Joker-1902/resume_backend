from pydantic import BaseModel, ConfigDict
from .models import Resume
from typing import Optional


class ResumeCreate(BaseModel):
    title: str
    content: str

class ResumeUpdate(BaseModel):
    title: Optional[str] | None = None
    content: Optional[str] | None = None


class ResumeInput(BaseModel):
    content: str

class ResumeInDB(BaseModel):
    id: int
    title: str
    content: str    

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):    
    email: Optional[str] | None = None
    password: Optional[str] | None = None


class UserInDB(BaseModel):
    id: int
    email: str
    hash_password: str

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str    