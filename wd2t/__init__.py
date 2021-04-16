from flask import Flask

from wd2t.decision import decision_blueprint
from wd2t.error_handlers import initialise_error_handlers


def init_app():
    app = Flask(__name__)
    # Load config here

    with app.app_context():

        initialise_error_handlers(app)

        app.register_blueprint(decision_blueprint)

        return app