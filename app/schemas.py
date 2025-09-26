from pydantic import BaseModel
from datetime import datetime

class BlogBase(BaseModel):
    title: str
    content: str

class BlogCreate(BlogBase):
    pass

class BlogResponse(BlogBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class BlogUpdate(BlogBase):
    pass