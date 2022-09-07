"""The create app module for creating a flask api application"""
from flask import Flask


from ..api.controller import predictions_app
from ..api.config import get_logger

_logger = get_logger(logger_name=__name__)

# xTODO: move that to an environment variable, maybe with conteinerization
API_NAME = 'houses_ml_api'

def create_app(*, config_object) -> Flask:
    """Create the app"""
    flask_app = Flask('houses_ml_api')
    flask_app.config.from_object(config_object)

    flask_app.register_blueprint(predictions_app)
    _logger.debug("Application instance created")

    return flask_app
