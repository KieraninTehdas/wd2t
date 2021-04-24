from unittest import mock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from wd2t.dependencies import get_tag_repository
from wd2t.main import app
from wd2t.repositories import TagRepository

client = TestClient(app)
tag_collection_mock = mock.Mock(spec_set=Collection)
app.dependency_overrides[get_tag_repository] = lambda: TagRepository(
    {"tags": tag_collection_mock}
)


def test_get_tags_by_key_starts_with():
    tags = [{"_id": str(uuid4()), "key": "Yale", "value": "50p"}]
    tag_collection_mock.find.return_value = (t for t in tags)
    key_starts_with = "som"

    result = client.get(f"/tags/?key_starts_with={key_starts_with}")

    assert result.status_code == 200
    assert result.json() == tags
    tag_collection_mock.find.assert_called_once_with(
        {"key": {"$regex": f"^{key_starts_with}.*", "$options": "i"}}
    )
