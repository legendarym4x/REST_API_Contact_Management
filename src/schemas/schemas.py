from datetime import date, datetime

from pydantic import BaseModel, EmailStr


class ContactModel(BaseModel):
    name: str
    surname: str
    email: EmailStr
    phone: str
    birthday: datetime


class ContactResponse(BaseModel):
    id: int = 1
    name: str
    surname: str
    email: EmailStr
    phone: str
    birthday: date
    created_at: datetime

    class Config:
        orm_mode = True
