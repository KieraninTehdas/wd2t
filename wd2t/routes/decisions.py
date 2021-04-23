from typing import List

import pytest
from fastapi import APIRouter, Depends, HTTPException
from wd2t.dependencies import get_decision_repository, get_tag_repository
from wd2t.models import Decision, DecisionBase
from wd2t.repositories import DecisionRepository, TagRepository

router = APIRouter(prefix="/decisions", tags=["decisions"])


@router.post("/", response_model=Decision)
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

    print(f"Creating {len(tags_to_create)} new tags")

    for tag in tags_to_create:
        tag_repo.save(tag.dict())

    return decision_repo.save(decision.dict())


@router.get("/{decision_id}", response_model=Decision)
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


@router.get("/", response_model=List[Decision])
def get_decisions(decision_repo: DecisionRepository = Depends(get_decision_repository)):
    return decision_repo.get_all()
