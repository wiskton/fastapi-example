from typing import Optional
from typing import List

from pydantic import BaseModel, EmailStr


class UserSchemaBase(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    is_admin: bool = False

    class Config:
        orm_mode = True


class UserSchemaCreate(UserSchemaBase):
    password: str


class UserSchemaUpdate(UserSchemaBase):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    is_admin: Optional[bool]
