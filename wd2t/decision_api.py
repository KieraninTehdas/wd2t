from datetime import date

from wd2t import config, tag_api
from wd2t.repositories import DecisionRepository

from marshmallow import Schema, fields, schema
from marshmallow.utils import EXCLUDE
from flask import Blueprint, make_response, jsonify, request

decision_blueprint = Blueprint("decision_blueprint", __name__, url_prefix="/decisions")

decision_repository = DecisionRepository(config.get_database())


class TagSchema(Schema):
    key = fields.Str(required=True)
    value = fields.Str(required=True)


class DecisionSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str()
    tags = fields.List(fields.Nested(TagSchema()))
    decided_on = fields.Date(missing=date.today())


schema = DecisionSchema(unknown=EXCLUDE)


@decision_blueprint.route("/", methods=["GET"])
def get_decisions():
    return make_response(jsonify(decision_repository.get_all()), 200)


@decision_blueprint.route("/<decision_id>", methods=["GET"])
def get_decision_by_id(decision_id):
    decision = decision_repository.get_by_id(decision_id)

    if not decision:
        return make_response(
            jsonify({"error": f"Decision {decision_id} not found"}), 404
        )

    return make_response(jsonify(decision), 200)


@decision_blueprint.route("/", methods=["POST"])
def create_decision():
    new_decision = request.json
    serialised_decision = schema.load(new_decision)

    result = decision_repository.save(schema.dump(serialised_decision))
    tag_api.create_tags(result["tags"])
    return make_response(jsonify(result), 200)
