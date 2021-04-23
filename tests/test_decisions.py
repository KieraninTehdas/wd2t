import json
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
    url_prefix = "/decisions"
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
        self.decision_collection_mock = mock.Mock(spec_set=Collection)
        self.tag_collection_mock = mock.Mock(spec_set=Collection)
        app.dependency_overrides[get_decision_repository] = lambda: DecisionRepository(
            {"decisions": self.decision_collection_mock}
        )
        app.dependency_overrides[get_tag_repository] = lambda: TagRepository(
            {"tags": self.tag_collection_mock}
        )

    def test_get_decision_by_id(self):
        self.decision_collection_mock.find_one.return_value = self.decision

        response = self.client.get(f"{self.url_prefix}/{self.decision_id}/")

        assert response.status_code == 200
        assert response.json() == self.serialied_decision
        assert {
            "_id": UUID(self.decision_id)
        } == self.decision_collection_mock.find_one.call_args_list[0][0][0]
        # For some reason this is failing with a weird assertion. Maybe due to inheritance.
        # Above does the same job less elegantly...
        # assert self.decision_collection_mock.find_one.assert_called_once_with(
        #    {"_id": UUID(self.decision_id)}
        # )

    def test_get_decision_by_id_when_not_found(self):
        self.decision_collection_mock.find_one.return_value = []

        response = self.client.get(f"{self.url_prefix}/{self.decision_id}/")

        assert response.status_code == 404

    def test_get_decisions(self):
        self.decision_collection_mock.find.return_value = [self.decision, self.decision]

        response = self.client.get(f"{self.url_prefix}/")

        assert response.status_code == 200
        assert response.json() == [self.serialied_decision, self.serialied_decision]

    def test_create_decision(self):
        tag_id = str(uuid4())
        preexisting_tag = {"key": "this_tag", "value": "exists"}
        new_tag = {"key": "thing_tag", "value": "needs_creating"}
        create_decision_request = {
            "title": "A decision",
            "description": "A thing we decided on",
            "tags": [preexisting_tag, new_tag],
        }
        created_decision = {**create_decision_request, "_id": self.decision_id}
        self.decision_collection_mock.save.return_value = created_decision
        self.tag_collection_mock.save.side_effect = lambda x: {**x, "_id": tag_id}
        self.tag_collection_mock.find_one.side_effect = lambda x: {
            preexisting_tag["key"]: preexisting_tag,
            new_tag["key"]: None,
            tag_id: new_tag,
        }[x.get("key", tag_id)]
        response = self.client.post(f"{self.url_prefix}/", json=create_decision_request)

        assert response == 200
