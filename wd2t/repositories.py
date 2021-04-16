from bson.objectid import ObjectId
from pymongo.database import Database


class TagRepository:
    def __init__(self, db: Database) -> None:
        self.collection = db.tags

    def save_tag(self, tag: dict):
        return self.collection.insert_one(tag).inserted_id

    def get_tag_by_id(self, tag_id: str) -> dict:
        return self.collection.find_one({"_id": ObjectId(tag_id)})


class AdrRepository:
    def __init__(self, db: Database) -> None:
        self.collection = db.adrs

    def save_adr(self, adr: dict):
        insert_result_id = self.collection.insert_one(adr).inserted_id

        if insert_result_id:
            return self.collection.find_one({"_id": ObjectId(insert_result_id)})
        else:
            return None