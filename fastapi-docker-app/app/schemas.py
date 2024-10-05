# app/schemas.py

from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    name: str
    completion_status: bool = False


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
