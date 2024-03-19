from pydantic import BaseModel


class CommentRead(BaseModel):
    id: int
    body: str
    author_id: int
    task_id: int

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    body: str


class CommentUpdate(BaseModel):
    id: int
    body: str
    is_moderated: bool
