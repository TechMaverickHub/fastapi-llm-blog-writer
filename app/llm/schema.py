from typing import List

from pydantic import BaseModel


class TopicKeyword(BaseModel):
    topics: List[str]