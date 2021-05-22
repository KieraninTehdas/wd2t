from typing import List, Union
from uuid import UUID, uuid4

from pymongo.database import Collection, Database

from wd2t.datetime_utils import get_utc_now


class MongoDbCrudRepository:
    def __init__(self, db: Database, collection_name: str) -> None:
        self.collection: Collection = db[collection_name]

    @staticmethod
    def _convert_to_uuid(_id: Union[str, UUID]) -> UUID:
        if isinstance(_id, UUID):
            return _id
        elif isinstance(_id, str):
            return UUID(_id)
        else:
            raise TypeError(
                f"Cannot convert unsupported id of type {type(_id)} to uuid"
            )

    def save(self, document: dict) -> str:
        document["_id"] = uuid4()
        result = self.collection.insert_one(document)

        return result.inserted_id

    def save_and_return_entity(self, document) -> dict:
        saved_entity_id = self.save(document)
        if saved_entity_id:
            return self.get_by_id(saved_entity_id)
        else:
            return None

    def get_by_id(self, _id: Union[str, UUID]) -> dict:
        return self.collection.find_one({"_id": self._convert_to_uuid(_id)})

    # TODO: Pagination!
    def get_all(self) -> List:
        return list(self.collection.find())

    def _query(self, query_params: dict) -> List:
        return list(self.collection.find(query_params))

    def delete(self, _id: Union[str, UUID]):
        self.collection.delete_one({"_id": self._convert_to_uuid(_id)})


class TagRepository(MongoDbCrudRepository):
    def __init__(self, db: Database) -> None:
        super().__init__(db, "tags")

    def find_by_key_starts_with(self, key_fragment: str) -> List[dict]:
        return self._query({"key": {"$regex": f"^{key_fragment}.*", "$options": "i"}})

    def find_one(self, tag_key: str, tag_value: str) -> dict:
        return self.collection.find_one({"key": tag_key, "value": tag_value})


class DecisionRepository(MongoDbCrudRepository):
    def __init__(self, db: Database) -> None:
        super().__init__(db, "decisions")

    def save_and_return_entity(self, decision_document: dict) -> dict:
        decision_document["documented_at"] = get_utc_now()
        try:
            decision_document["decided_on"] = decision_document[
                "decided_on"
            ].isoformat()
        except AttributeError:
            pass
        return super().save_and_return_entity(decision_document)
