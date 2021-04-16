import flask
import marshmallow.exceptions


def handle_validation_error(e: marshmallow.exceptions.ValidationError):
    response = flask.jsonify(e.normalized_messages())
    response.status_code = 400
    return response


def initialise_error_handlers(app):
    app.register_error_handler(
        marshmallow.exceptions.ValidationError, handle_validation_error
    )
