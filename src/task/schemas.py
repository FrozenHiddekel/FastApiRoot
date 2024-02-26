from pydantic import BaseModel, EmailStr


class TaskCreate(BaseModel):
    title: str
    description: str
    executor_email: EmailStr
    priority: int


class TaskUpdate(BaseModel):
    id: int
    title: str
    description: str
    executor_email: EmailStr
    priority: int
