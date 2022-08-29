"""The flask controller module for the houses api server"""
from flask import Blueprint, request, jsonify

from houses_pipeline.predict import lasso
from .config import get_logger

_logger = get_logger(logger_name=__name__)

predictions_app = Blueprint('predictions_app', __name__)

@predictions_app.get('/health')
def get_health():
    """Get whether the api is in good health or is on medications"""
    return "OK"


@predictions_app.get("/version/<name>")
def get_version(name: str):
    """The version of the model"""
    return f"OK Boomer, {name}"


@predictions_app.post("/predict/lasso")
def get_lasso_predictions():
    """pass an observation or more and return an array of predictions"""
    input_data = request.get_json()

    _logger.info("Input %s", input_data)

    # validate, preprocess and get predictions using the fitted model
    prediction_results = lasso.predict(input_data=input_data)
    _logger.info("Outputs: %s", prediction_results)
    _logger.info(jsonify(prediction_results))
    return jsonify(prediction_results)


# @predictions_app.errorhandler(404)
# def not_found(error):
#     resp = make_response(render_template('error.html'), 404)
#     resp.headers['X-Something'] = 'A value'
#     return resp
