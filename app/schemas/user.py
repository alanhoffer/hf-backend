from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    role: str
    created_at: datetime

    class Config:
        orm_mode = True