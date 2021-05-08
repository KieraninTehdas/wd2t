from typing import List, Optional

from fastapi import APIRouter, Response, status
from fastapi.params import Depends
from wd2t.dependencies import get_tag_repository
from wd2t.models import Tag, TagBase
from wd2t.repositories import TagRepository

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("/", response_model=Tag)
def create_tag(tag: TagBase, tag_repo: TagRepository = Depends(get_tag_repository)):
    return tag_repo.save_and_return_entity(tag.dict())


@router.get("/", response_model=List[Tag])
def get_tags(
    key_starts_with: Optional[str] = None,
    tag_repo: TagRepository = Depends(get_tag_repository),
):
    if key_starts_with:
        return tag_repo.find_by_key_starts_with(key_starts_with)
    else:
        return tag_repo.get_all()


@router.delete("/{tag_id}", response_model=None)
def delete_tag(tag_id: str, tag_repo: TagRepository = Depends(get_tag_repository)):
    tag_repo.delete(tag_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
