from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class BookSchema(BaseModel):
    title: str
    author: str
    genre: str
    availability: int

class BookUpdateSchema(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    availability: Optional[int] = None