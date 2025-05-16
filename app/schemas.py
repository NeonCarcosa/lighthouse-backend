from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional
from enum import Enum

class BiasEnum(str, Enum):
    LEFT = "LEFT"
    LEAN_LEFT = "LEAN_LEFT"
    CENTER = "CENTER"
    LEAN_RIGHT = "LEAN_RIGHT"
    RIGHT = "RIGHT"

class SourceSchema(BaseModel):
    id: UUID
    name: str
    url: Optional[str]
    bias_label: BiasEnum

    class Config:
        orm_mode = True

class ArticleSchema(BaseModel):
    id: UUID
    title: str
    summary: Optional[str]
    url: str
    published_at: datetime
    source: SourceSchema

    class Config:
        orm_mode = True
