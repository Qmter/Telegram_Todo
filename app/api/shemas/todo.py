from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CreateTodo(BaseModel):
    title: str = Field(..., max_length=50, min_length=10)
    description: Optional[str] = Field(None, max_length=255)
    user_id: int


class ResponseTodo(BaseModel):
    title: str = Field(..., max_length=50, min_length=10)
    description: Optional[str] = Field(None, max_length=255)
    created_at: datetime
    complete: bool

class ChangeTodo(BaseModel):
    id_task: int
    title: str = Field(..., max_length=50, min_length=10)
    description: Optional[str] = Field(None, max_length=255)

