from datetime import date, datetime
from unittest import mock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from pymongo.collection import Collection
from wd2t.dependencies import get_decision_repository, get_tag_repository
from wd2t.main import app
from wd2t.repositories import DecisionRepository, TagRepository


class TestDecisions:
    client = TestClient(app)
    decision_id = str(uuid4())
    now = datetime.utcnow()
    today = date.today()
    url_prefix = "/wd2t/decisions"
    decision = {
        "_id": decision_id,
        "title": "A decision",
        "description": "Something we decided",
        "tags": [],
        "documented_at": now,
        "decided_on": today,
    }
    serialied_decision = {
        **decision,
        "documented_at": now.isoformat(),
        "decided_on": today.isoformat(),
    }

    @pytest.fixture(autouse=True)
    def run_around_test(self):
        self.decision_repo_mock: DecisionRepository = mock.Mock(
            spec_set=DecisionRepository
        )
        self.tag_repo_mock: TagRepository = mock.Mock(spec_set=TagRepository)
        app.dependency_overrides[
            get_decision_repository
        ] = lambda: self.decision_repo_mock
        app.dependency_overrides[get_tag_repository] = lambda: self.tag_repo_mock

    def test_get_decision_by_id(self):
        self.decision_repo_mock.get_by_id.return_value = self.decision

        response = self.client.get(f"{self.url_prefix}/{self.decision_id}/")

        assert response.status_code == 200
        assert response.json() == self.serialied_decision
        self.decision_repo_mock.get_by_id.assert_called_once_with(self.decision_id)

    def test_get_decision_by_id_when_not_found(self):
        self.decision_repo_mock.get_by_id.return_value = []

        response = self.client.get(f"{self.url_prefix}/{self.decision_id}/")

        assert response.status_code == 404
        self.decision_repo_mock.get_by_id.assert_called_once_with(self.decision_id)

    def test_get_decisions(self):
        self.decision_repo_mock.get_all.return_value = [self.decision, self.decision]

        response = self.client.get(f"{self.url_prefix}/")

        assert response.status_code == 200
        assert response.json() == [self.serialied_decision, self.serialied_decision]
        self.decision_repo_mock.get_all.assert_called_once()

    def test_create_decision(self):
        preexisting_tag = {"key": "this_tag", "value": "exists"}
        new_tag = {"key": "thing_tag", "value": "needs_creating"}
        create_decision_request = {
            "title": "A decision",
            "description": "A thing we decided on",
            "tags": [preexisting_tag, new_tag],
        }
        created_decision = {
            **create_decision_request,
            "_id": self.decision_id,
            "documented_at": self.now.isoformat(),
            "decided_on": self.today.isoformat(),
        }
        self.tag_repo_mock.find_one.side_effect = [preexisting_tag, None]
        self.decision_repo_mock.save_and_return_entity.return_value = created_decision

        response = self.client.post(f"{self.url_prefix}/", json=create_decision_request)

        assert response.status_code == 200
        assert response.json() == created_decision
        assert self.tag_repo_mock.find_one.call_count == 2
        self.tag_repo_mock.save.assert_called_once_with(new_tag)
        self.decision_repo_mock.save_and_return_entity.assert_called_once_with(
            {**create_decision_request, "decided_on": self.today}
        )
