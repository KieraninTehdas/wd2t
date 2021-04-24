from datetime import datetime
from typing import List, Union
from uuid import UUID, uuid4

from pymongo.database import Collection, Database


class MongoDbCrudRepository:
    def __init__(self, db: Database, collection_name: str) -> None:
        self.collection: Collection = db[collection_name]

    def save(self, document) -> str:
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
        if isinstance(_id, str):
            try:
                _id = UUID(_id)
            except ValueError:
                return None
        return self.collection.find_one({"_id": _id})

    # TODO: Pagination!
    def get_all(self) -> List:
        return list(self.collection.find())

    def query(self, query_params: dict) -> List:
        return list(self.collection.find(query_params))


class TagRepository(MongoDbCrudRepository):
    def __init__(self, db: Database) -> None:
        super().__init__(db, "tags")

    def find_by_key_starts_with(self, key_fragment: str) -> List:
        return super().query({"key": {"$regex": f"^{key_fragment}.*", "$options": "i"}})

    def find_one(self, tag_key: str, tag_value: str):
        return self.collection.find_one({"key": tag_key, "value": tag_value})


class DecisionRepository(MongoDbCrudRepository):
    def __init__(self, db: Database) -> None:
        super().__init__(db, "decisions")

    def save_and_return_entity(self, decision_document: dict) -> dict:
        decision_document["documented_at"] = datetime.utcnow()
        return super().save_and_return_entity(decision_document)
