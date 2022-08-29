"""
Preprocess the input data to generate a ready to use dataset
in the modelling step of the pipeline
"""
# general utilities
import logging
import pandas as pd
import numpy as np
import click

# sklearn pipeline modules
# internal modules
from houses_pipeline import constants
from houses_pipeline.config.logging import LoggingHandler
from houses_pipeline.preprocess.core import load_preprocess_pipeline


logger = LoggingHandler.get_logger(__name__)

@click.command()
@click.argument(
    'input_filepath',
    type=click.Path(exists=True),
    default=constants.DEFAULT_PREPROCESS_INPUT_PATH
)
@click.argument(
    'output_filepath',
    type=click.Path(),
    default=constants.DEFAULT_PREPROCESS_OUTPUT_PATH
)
@click.option(
    '-v',
    '--verbose',
    'verbose',
    required=False,
    default=False,
    help=constants.VERBOSE_HELP
)
def main(input_filepath: str, output_filepath: str, verbose: bool):
    """Preprocess the dataset and turn it from the given input to the output"""
    # click.echo() or logger.info?
    logger.info("Transforming %s to %s", input_filepath, output_filepath)

    # load the input dataframe
    input_df = pd.read_csv(input_filepath)

    # load the pipeline to preprocess the data
    pipeline = load_preprocess_pipeline(verbose=verbose)

    # transform the data
    to_impute = np.append(constants.CATEGORICAL_COLUMNS, constants.ORDINALS)
    output_houses_dataframe = pipeline.fit_transform(
        input_df,
        impute_missing_categories__columns=to_impute
    )

    # save the output to the specified path
    output_houses_dataframe.to_csv(output_filepath, index=False)

if __name__ == '__main__':
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    # pylint: disable=no-value-for-parameter
    main()
