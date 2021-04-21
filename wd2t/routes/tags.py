from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from wd2t.dependencies import get_tag_repository
from wd2t.models import Tag, TagBase
from wd2t.repositories import TagRepository

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("/", response_model=Tag)
def create_tag(tag: TagBase, tag_repo: TagRepository = Depends(get_tag_repository)):
    return tag_repo.save(tag.dict())


@router.get("/", response_model=List[Tag])
def get_tags_by_key_starts_with(
    key_starts_with: str, tag_repo: TagRepository = Depends(get_tag_repository)
):
    return tag_repo.find_by_key_starts_with(key_starts_with)
