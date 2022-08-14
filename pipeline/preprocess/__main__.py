"""
Provides some arithmetic functions
"""
import logging
import pandas as pd
import click
from sklearn.pipeline import Pipeline

from pipeline.preprocess import constants
from pipeline.preprocess.core import preprocessing_steps


@click.command()
@click.argument(
    'input_filepath',
    type=click.Path(exists=True),
    default="data/raw/train.csv"
)
@click.argument(
    'output_filepath',
    type=click.Path(),
    default="data/interim/train.csv"
)
@click.option(
    '-v',
    '--verbose',
    'verbose',
    required=False,
    default=False
)
def main(input_filepath, output_filepath, verbose):
    """Preprocess the dataset and turn it from the given input to the output"""
    logger = logging.getLogger(__name__)
    logger.info("Transforming %s to %s", input_filepath, output_filepath)

    # load the input dataframe
    input_df = pd.read_csv(input_filepath)

    # pass it through the pipeline
    pipeline = Pipeline(steps=preprocessing_steps, verbose=verbose)
    output_houses_dataframe = pipeline.fit_transform(
        X=input_df,
        impute_missing_categories__columns=constants.CATEGORICAL_COLUMNS,
        ordinals_encoding__columns=constants.ORDINALS,
        remove_redundant_columns__additional=['GarageYrBlt', 'Exterior2nd']
    )

    # write the output to the specified path
    output_houses_dataframe.to_csv(output_filepath)

if __name__ == '__main__':
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    # pylint: disable=no-value-for-parameter
    main()
