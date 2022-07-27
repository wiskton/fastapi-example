from typing import Optional

from sqlmodel import Field, SQLModel
from sqlalchemy import UniqueConstraint, Column, String


class UserModel(SQLModel, table=True):
    __tablename__: str = 'users'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(sa_column=Column("email", String, unique=True))
    password: str
    is_admin: bool