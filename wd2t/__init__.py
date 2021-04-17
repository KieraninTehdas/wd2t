from datetime import datetime, date
from typing import Any

from flask import Flask
from flask.json import JSONEncoder

from wd2t import config
from wd2t.decision_api import decision_blueprint
from wd2t.tag_api import tag_blueprint
from wd2t.error_handlers import initialise_error_handlers


class ISO8601DateTimeEncoder(JSONEncoder):
    def default(self, o: Any):
        if isinstance(o, datetime) or isinstance(o, date):
            return o.isoformat()
        return super().default(o)


def init_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)

    app.json_encoder = ISO8601DateTimeEncoder

    with app.app_context():

        initialise_error_handlers(app)

        app.register_blueprint(decision_blueprint)
        app.register_blueprint(tag_blueprint)

        return app