from datetime import datetime
from typing import Union
from uuid import UUID, uuid4

from pymongo.database import Database, Collection


class MongoDbCrudRepository:
    # TODO: Pagination!
    def __init__(self, db: Database, collection_name: str) -> None:
        self.collection: Collection = db[collection_name]

    def save(self, document):
        document["_id"] = uuid4()
        result = self.collection.insert_one(document)

        if result:
            return self.get_by_id(result.inserted_id)
        else:
            return None

    def get_by_id(self, _id: Union[str, UUID]):
        if isinstance(_id, str):
            _id = UUID(_id)

        return self.collection.find_one({"_id": _id})

    def get_all(self):
        return list(self.collection.find())


class TagRepository(MongoDbCrudRepository):
    def __init__(self, db: Database) -> None:
        super().__init__(db, "tags")


class DecisionRepository(MongoDbCrudRepository):
    def __init__(self, db: Database) -> None:
        super().__init__(db, "decisions")

    def save(self, decision_document):
        decision_document["documented_at"] = datetime.utcnow()
        return super().save(decision_document)
