from datetime import datetime
from unittest import mock
from uuid import UUID, uuid4

import pytest
from pymongo.collection import Collection
from pymongo.results import InsertOneResult
from wd2t.repositories import DecisionRepository, MongoDbCrudRepository, TagRepository


class TestMongoDbCrudRepository:
    _id = uuid4()
    document = {"something": "in a self.document"}
    document_with_id = {"_id": _id, **document}

    @pytest.fixture(autouse=True)
    def run_around_test(self):
        self.collection_mock = mock.Mock(spec_set=Collection)
        self.repo = MongoDbCrudRepository({"test": self.collection_mock}, "test")

    @mock.patch("wd2t.repositories.uuid4", return_value=_id)
    def test_save(self, _):
        self.collection_mock.insert_one.return_value = InsertOneResult(self._id, True)

        result = self.repo.save(self.document)

        assert result == self._id
        self.collection_mock.insert_one.assert_called_once_with(self.document_with_id)

    @mock.patch("wd2t.repositories.uuid4", return_value=_id)
    def test_save_and_return_entity(self, _):
        self.collection_mock.insert_one.return_value = InsertOneResult(self._id, True)
        self.collection_mock.find_one.return_value = self.document_with_id

        result = self.repo.save_and_return_entity(self.document)

        assert result == self.document_with_id
        self.collection_mock.insert_one.assert_called_once_with(self.document_with_id)
        self.collection_mock.find_one.assert_called_once_with({"_id": self._id})

    @mock.patch("wd2t.repositories.uuid4", return_value=_id)
    def test_save_and_return_entity_when_fails(self, _):
        self.collection_mock.insert_one.return_value = InsertOneResult(None, False)

        result = self.repo.save_and_return_entity(self.document)

        assert result == None
        self.collection_mock.insert_one.assert_called_once_with(self.document_with_id)
        self.collection_mock.find_one.assert_not_called()

    @pytest.mark.parametrize("test_input", [(str(_id)), _id])
    def test_get_by_id(self, test_input):
        self.repo.get_by_id(test_input)

        self.collection_mock.find_one.assert_called_once_with({"_id": self._id})

    def test_get_all(self):
        self.collection_mock.find.return_value = []

        self.repo.get_all()

        self.collection_mock.find.assert_called_once_with()

    @pytest.mark.parametrize("test_input", [(str(_id)), (_id)])
    def test_delete(self, test_input):
        self.repo.delete(test_input)

        self.collection_mock.delete_one.assert_called_once_with({"_id": self._id})

    def test_query(self):
        self.collection_mock.find.return_value = []
        search_params = {"some": "param"}

        self.repo._query(search_params)

        self.collection_mock.find.assert_called_once_with(search_params)


class TestTagRepository:
    @pytest.fixture(autouse=True)
    def run_around_test(self):
        self.collection_mock = mock.Mock(spec_set=Collection)
        self.repo = TagRepository({"tags": self.collection_mock})

    def test_find_by_key_starts_with(self):
        self.collection_mock.find.return_value = []
        key_fragment = "sta"
        expected_query_params = {
            "key": {"$regex": f"^{key_fragment}.*", "$options": "i"}
        }

        self.repo.find_by_key_starts_with(key_fragment)

        self.collection_mock.find.assert_called_once_with(expected_query_params)

    def test_find_one(self):
        tag_key = "the key"
        tag_value = "the value"

        self.repo.find_one(tag_key, tag_value)

        self.collection_mock.find_one.assert_called_once_with(
            {"key": tag_key, "value": tag_value}
        )


class TestDecisionRepository:
    now = datetime.utcnow()
    today = now.date()

    @pytest.fixture(autouse=True)
    def run_around_test(self):
        self.collection_mock = mock.Mock(spec_set=Collection)
        self.repo = DecisionRepository({"decisions": self.collection_mock})

    @mock.patch("wd2t.repositories.get_utc_now", return_value=now)
    @mock.patch("wd2t.repositories.uuid4")
    def test_save_and_return_entity(self, _, uuid_patch):
        _id = uuid4()
        uuid_patch.return_value = _id
        document = {"some_document": "i am", "decided_on": self.today}

        self.repo.save_and_return_entity(document)

        self.collection_mock.insert_one.assert_called_once_with(
            {"_id": _id, "documented_at": self.now, **document}
        )

    @mock.patch("wd2t.repositories.get_utc_now", return_value=now)
    @mock.patch("wd2t.repositories.uuid4")
    def test_save_and_return_entity(self, uuid_patch, _):
        _id = uuid4()
        uuid_patch.return_value = _id
        document = {"some_document": "i am", "decided_on": self.today}
        document_with_id = {
            **document,
            "_id": _id,
            "documented_at": self.now,
            "decided_on": self.today.isoformat(),
        }
        self.collection_mock.insert_one.return_value = InsertOneResult(_id, True)
        self.collection_mock.find_one.return_value = document_with_id

        result = self.repo.save_and_return_entity(document)

        assert result == document_with_id
        self.collection_mock.insert_one.assert_called_once_with(document_with_id)
        self.collection_mock.find_one.assert_called_once_with({"_id": _id})
