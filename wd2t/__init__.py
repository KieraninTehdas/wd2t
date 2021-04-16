from flask import Flask

from wd2t import config
from wd2t.decision import decision_blueprint
from wd2t.error_handlers import initialise_error_handlers


db = config.get_database()


def init_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)

    with app.app_context():

        initialise_error_handlers(app)

        app.register_blueprint(decision_blueprint)

        return app