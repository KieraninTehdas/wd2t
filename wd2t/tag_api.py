from typing import List

from flask import Blueprint, request
from flask.helpers import make_response
from flask.json import jsonify
from marshmallow import Schema, fields
from marshmallow.utils import EXCLUDE

from wd2t import config
from wd2t.repositories import TagRepository

tag_blueprint = Blueprint("tag_blueprint", __name__, url_prefix="/tags")

tag_repository = TagRepository(config.get_database())


class TagSchema(Schema):
    key = fields.Str(required=True)


schema = TagSchema(unknown=EXCLUDE)


@tag_blueprint.route("/", methods=["GET"], strict_slashes=False)
def find_tags_by_key_starts_with():
    try:
        key_fragment = request.args["key_starts_with"]
    except KeyError:
        return make_response(jsonify([]), 200)

    return make_response(
        jsonify(list(tag_repository.find_by_key_starts_with(key_fragment))), 200
    )


def create_tags(tags: List[dict]):
    tags_to_create = [
        tag for tag in tags if tag_repository.find(tag["key"], tag["value"]) is None
    ]

    for tag in tags_to_create:
        tag_repository.save(tag)
