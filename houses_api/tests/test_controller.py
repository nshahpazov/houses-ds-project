"""Controller setup for the testing context"""
import os
import json
import math
import pandas as pd
from houses_pipeline import __version__ as _model_version
from .. import __version__ as _api_version

from ..api.config import get_logger
from ..api.config import TEST_DATASET_PATH



_logger = get_logger(logger_name=__name__)

def test_health_endpoint_returns_ok_status(test_client):
    """
    test whether health returns an HTTP 200 ok status
    The testing in flask uses pytest fixtures to emulate a running server
    without actually running a server, but using a testing context, having
    everything which is in the web server responses.
    """
    response = test_client.get('/health')
    _logger.info("Health returns OK http status")
    assert response.status_code == 200


def test_version_endpoint_returns_version(test_client):
    """
    Test whether the API is returning proper version of the model and the API
    """
    # When
    response = test_client.get('/version')

    # Then
    assert response.status_code == 200
    response_json = json.loads(response.data)
    assert response_json['model_version'] == _model_version
    assert response_json['api_version'] == _api_version


def test_prediction_endpoint_returns_prediction(test_client):
    """
    Given
    Load the test data from the regression_model package
    This is important as it makes it harder for the test
    data versions to get confused by not spreading it
    across packages.
    """

    # fetch data
    os.system("./houses_pipeline/fetch/fetch_dataset.sh data/raw")

    # preprocess
    os.system("python -m houses_pipeline.preprocess")
    os.system(
        "python -m houses_pipeline.preprocess data/raw/test.csv data/interim/test.csv"
    )

    # train a model
    os.system("python -m houses_pipeline.modelling.train_lasso")

    test_data = pd.read_csv(TEST_DATASET_PATH)
    post_json = test_data[0:1].to_json(orient='records')
    # when
    response = test_client.post('/predict/lasso', json=json.loads(post_json))

    # then
    assert response.status_code == 200
    response_json = json.loads(response.data)
    prediction = response_json['predictions']
    print(response_json)
    response_version = response_json['version']
    assert math.ceil(prediction[0]) == 117205
    assert response_version == _model_version
