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
    decided_on: Optional[date] = Field(default=date.today(), alias="decidedOn")

    class Config:
        allow_population_by_field_name = True


class Decision(DecisionBase):
    id: UUID4 = Field(alias="_id")
    documented_at: datetime = Field(alias="documentedAt")
