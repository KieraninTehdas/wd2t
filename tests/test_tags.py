from unittest import mock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from pymongo.collection import Collection
from wd2t.dependencies import get_tag_repository
from wd2t.main import app
from wd2t.repositories import TagRepository


class TestTags:
    client = TestClient(app)
    url_prefix = "/wd2t/tags"
    tag = {"_id": str(uuid4()), "key": "Yale", "value": "50p"}
    tags = [tag]

    @pytest.fixture(autouse=True)
    def run_around_test(self):
        self.tag_repo_mock: TagRepository = mock.Mock(spec_set=TagRepository)
        app.dependency_overrides[get_tag_repository] = lambda: self.tag_repo_mock

    def test_create_tag(self):
        create_tag_request = {k: v for k, v in self.tag.items() if k != "_id"}
        self.tag_repo_mock.save_and_return_entity.return_value = self.tag

        result = self.client.post(f"{self.url_prefix}/", json=create_tag_request)

        assert result.status_code == 200
        assert result.json() == self.tag
        self.tag_repo_mock.save_and_return_entity.assert_called_once_with(
            create_tag_request
        )

    def test_delete_tag(self):
        tag_id = "some_id"

        result = self.client.delete(f"{self.url_prefix}/{tag_id}")

        assert result.status_code == 204
        self.tag_repo_mock.delete.assert_called_once_with(tag_id)

    def test_get_tags(self):
        self.tag_repo_mock.get_all.return_value = self.tags

        result = self.client.get(f"{self.url_prefix}/")

        assert result.status_code == 200
        assert result.json() == self.tags
        self.tag_repo_mock.get_all.assert_called_once()

    def test_get_tags_by_key_starts_with(self):
        self.tag_repo_mock.find_by_key_starts_with.return_value = self.tags
        key_starts_with = "som"

        result = self.client.get(
            f"{self.url_prefix}/?key_starts_with={key_starts_with}"
        )

        assert result.status_code == 200
        assert result.json() == self.tags
        self.tag_repo_mock.find_by_key_starts_with.assert_called_once_with(
            key_starts_with
        )
