"""
Preprocess the input data to generate a ready to use dataset
in the modelling step of the pipeline
"""
# general utilities
import logging
import click

# sklearn pipeline modules
# internal modules
from houses_pipeline import constants
from houses_pipeline.config.logging import LoggingHandler
from houses_pipeline.preprocess.core import preprocess


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
    preprocess(input_filepath, output_filepath, verbose)

if __name__ == '__main__':
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    main()
