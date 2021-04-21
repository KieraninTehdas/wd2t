from datetime import date, datetime
from typing import List, Optional

from pydantic import Field
from pydantic.main import BaseModel
from pydantic.types import UUID4


class TagBase(BaseModel):
    key: str
    value: str


class Tag(TagBase):
    id: UUID4 = Field(alias="_id")


class DecisionBase(BaseModel):
    title: str
    description: Optional[str]
    tags: List[TagBase] = list()
    decided_on: date = date.today()


class Decision(DecisionBase):
    id: UUID4 = Field(alias="_id")
    documented_at: datetime
