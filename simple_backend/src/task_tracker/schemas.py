from enum import Enum
from pydantic import BaseModel, Field

class StatusEnum(str, Enum):
    pending = "pending"
    done = "done"
    in_progress = "in_progress"

class TaskBase(BaseModel):
    title: str = Field(..., example="Купить молоко")
    status: StatusEnum = Field(..., example="pending")

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True  # Для Pydantic v2: from_attributes = True
