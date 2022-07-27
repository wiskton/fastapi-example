from typing import Optional

from sqlmodel import Field, SQLModel


class CourseModel(SQLModel, table=True):
    __tablename__: str = 'courses'

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    hours: int

