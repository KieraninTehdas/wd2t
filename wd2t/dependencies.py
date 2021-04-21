from wd2t.config import get_database
from wd2t.repositories import DecisionRepository, TagRepository

decision_repository = DecisionRepository(get_database())
tag_repository = TagRepository(get_database())


def get_decision_repository() -> DecisionRepository:
    return decision_repository


def get_tag_repository() -> TagRepository:
    return tag_repository
