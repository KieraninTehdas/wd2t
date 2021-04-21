from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.params import Depends

from wd2t.config import get_database
from wd2t.models import Decision, DecisionBase, Tag, TagBase
from wd2t.repositories import DecisionRepository, TagRepository

app = FastAPI()

decision_repository = DecisionRepository(get_database())
tag_repository = TagRepository(get_database())


def get_decision_repository() -> DecisionRepository:
    return decision_repository


def get_tag_repository() -> TagRepository:
    return tag_repository


@app.post("/tags", response_model=Tag)
def create_tag(tag: TagBase, tag_repo: TagRepository = Depends(get_tag_repository)):
    return tag_repo.save(tag.dict())


@app.post("/decisions", response_model=Decision)
def create_decision(
    decision: DecisionBase,
    decision_repo: DecisionRepository = Depends(get_decision_repository),
    tag_repo: TagRepository = Depends(get_tag_repository),
):
    tags_to_create = [
        tag
        for tag in decision.tags
        if tag_repo.find_one(tag_key=tag.key, tag_value=tag.value) is None
    ]

    for tag in tags_to_create:
        tag_repo.save(tag.dict())

    return decision_repo.save(decision.dict())


@app.get("/decisions/{decision_id}", response_model=Decision)
def get_decision_by_id(
    decision_id: str,
    decision_repo: DecisionRepository = Depends(get_decision_repository),
):
    decision = decision_repo.get_by_id(decision_id)

    if not decision:
        raise HTTPException(
            status_code=404, detail=f"Decision with id {decision_id} not found"
        )

    return decision


@app.get("/decisions", response_model=List[Decision])
def get_decisions(decision_repo: DecisionRepository = Depends(get_decision_repository)):
    return decision_repo.get_all()


@app.get("/tags", response_model=List[Tag])
def get_tags_by_key_starts_with(
    key_starts_with: str, tag_repo: TagRepository = Depends(get_tag_repository)
):
    return tag_repo.find_by_key_starts_with(key_starts_with)
