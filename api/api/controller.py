"""The flask controller module for the houses api server"""
from flask import Blueprint, request, jsonify

from houses_pipeline.predict import lasso
from houses_pipeline import __version__ as _model_version
from houses_api import __version__ as _api_version
from houses_api.api.validation import validate_inputs


from .config import get_logger

_logger = get_logger(logger_name=__name__)

predictions_app = Blueprint('predictions_app', __name__)

@predictions_app.get('/health')
def get_health():
    """Get whether the api is in good health or is on medications"""
    return "OK"


@predictions_app.get('/version')
def version():
    """
    Return the version of the model and the Restful API
    """
    return {
        'model_version': _model_version,
        'api_version': _api_version
    }


@predictions_app.post("/predict/lasso")
def produce_lasso_predictions():
    """pass an observation or more and return an array of predictions"""
    input_data = request.get_json()

    _logger.info("Input %s", input_data)
    input_data, errors = validate_inputs(input_data=input_data)

    # validate, preprocess and get predictions using the fitted model
    prediction_results = lasso.predict(input_data=input_data)
    _logger.info("Outputs: %s", prediction_results)
    _logger.info(prediction_results)
    return jsonify(prediction_results | {'errors': errors})


# @predictions_app.errorhandler(404)
# def not_found(error):
#     resp = make_response(render_template('error.html'), 404)
#     resp.headers['X-Something'] = 'A value'
#     return resp
