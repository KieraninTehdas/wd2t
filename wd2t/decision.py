from typing import Iterable
from datetime import date, datetime
from uuid import uuid4

from jinja2.utils import missing
from wd2t import config
from wd2t.repositories import DecisionRepository

from marshmallow import Schema, fields, post_load, schema
from flask import Blueprint, make_response, jsonify, request, current_app
from marshmallow.utils import EXCLUDE, pprint

decision_blueprint = Blueprint("decision_blueprint", __name__, url_prefix="/decisions")

decision1 = {
    "title": "A very important decision",
    "id": "1",
    "description": "This was a very difficult decision to make",
    "tags": [{"key": "service_name", "value": "ABB"}],
}
decision2 = {
    "title": "Another important decision",
    "id": "2",
    "description": "This decision was easy",
}

decisions = [decision1, decision2]

decision_repository = DecisionRepository(config.get_database())


class Decision:
    def __init__(
        self, title: str, description: str, tags: Iterable, decided_on: date
    ) -> None:
        self._id = uuid4()
        self.title: str = title
        self.description: str = description
        self.tags: Iterable = tags
        self.decided_on: date = decided_on or date.today()
        self.documented_at: datetime = datetime.utcnow()


class Tag:
    def __init__(self, key: str, value: str) -> None:
        self.key = key
        self.value = value


class TagSchema(Schema):
    key = fields.Str(required=True)
    value = fields.Str(required=True)


class DecisionSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str()
    tags = fields.List(fields.Nested(TagSchema()))
    decided_on = fields.Date(missing=date.today())

    # @post_load
    # def construct_decision(self, data, **kwargs):
    #    return Decision(
    #        title=data["title"],
    #        description=data.get("description"),
    #        tags=data.get("tags"),
    #        decided_on=data.get("decided_on"),
    #    )


schema = DecisionSchema(unknown=EXCLUDE)


@decision_blueprint.route("/", methods=["GET"])
def get_decisions():
    return make_response(jsonify(decisions), 200)


@decision_blueprint.route("/<decision_id>", methods=["GET"])
def get_decision_by_id(decision_id):
    decision = [d for d in decisions if d["id"] == decision_id]

    if not decision:
        return make_response(jsonify(), 404)
    else:
        return make_response(jsonify(decision[0]), 200)


@decision_blueprint.route("/", methods=["POST"])
def create_decision():
    new_decision = request.json
    serialised_decision = schema.load(new_decision)

    result = decision_repository.save(schema.dump(serialised_decision))
    pprint(result)
    return make_response(jsonify(result), 200)
