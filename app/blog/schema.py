from datetime import datetime
from typing import List, TypeVar, Generic

from pydantic import BaseModel
from pydantic.generics import GenericModel


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


T = TypeVar("T")


class PaginatedResponse(GenericModel, Generic[T]):
    items: List[T]
    page: int
    limit: int
    total: int
    pages: int
