from datetime import datetime

from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    content: str

class BlogCreate(BlogBase):
    pass

class BlogResponse(BlogBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class BlogUpdate(BlogBase):
    pass