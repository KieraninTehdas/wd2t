import os
from typing import List

from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient
from pymongo.database import Database

load_dotenv(find_dotenv())


class Config:
    def __init__(self) -> None:
        self.root_url_prefix: str = os.environ.get("ROOT_URL_PREFIX", "/wd2t")
        self.allowed_origins: List[str] = [
            origin.strip()
            for origin in os.environ.get("ALLOWED_ORIGINS", "").split(",")
        ]


_mongo_username = os.environ.get("MONGO_USERNAME")
_mongo_password = os.environ.get("MONGO_PASSWORD")

_mongo_client = MongoClient(
    "localhost",
    username=_mongo_username,
    password=_mongo_password,
    authSource="wd2t",
)


def get_database() -> Database:
    return _mongo_client.wd2t
