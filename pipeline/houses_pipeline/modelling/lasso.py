"""Train a lasso regression. Intended use is as a command from the terminal"""
# generally used modules
from urllib.parse import urlparse
import joblib
import pandas as pd
import click

# pipeline feature engineering and scaling
from sklearn.compose import TransformedTargetRegressor, ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PowerTransformer, OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.impute import SimpleImputer

# modeling
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split

# model tracking
import mlflow
import mlflow.sklearn

# internal modules
from houses_pipeline import constants
from houses_pipeline.transformers import RareCategoriesReplacer
from houses_pipeline import __version__
from houses_pipeline.config import config
from houses_pipeline.config.logging import LoggingHandler

_logger = LoggingHandler.get_logger(__name__)

__ordinal_encoder = OrdinalEncoder(
    categories=[constants.ORDINALS_ORDERING] * len(constants.ORDINALS),
    handle_unknown='use_encoded_value',
    unknown_value=-1
)

@click.command()
@click.argument(
    'input_filepath',
    type=click.Path(exists=True),
    default=constants.DEFAULT_TRAIN_INPUT_PATH
)
@click.option(
    '--alpha',
    'alpha',
    required=False,
    default=constants.DEFAULT_LASSO_ALPHA,
    help="Regularization parameter of the lasso regression"
)
@click.option(
    '--model_seed',
    'model_seed',
    required=False,
    default=constants.DEFAULT_MODEL_SEED,
    help="Regularization model seed"
)
@click.option(
    '--split_seed',
    'split_seed',
    required=False,
    default=1,
    help="Splitting seed"
)
@click.option(
    '--train_size',
    'train_size',
    required=False,
    default=constants.DEFAULT_TRAIN_SET_SIZE,
    help="Train set size to be used for the training"
)
@click.option(
    '--rare_threshold',
    'rare_threshold',
    required=False,
    default=0.05,
    help="Rare Threshold"
)
def main(
    input_filepath, alpha, model_seed, split_seed, train_size, rare_threshold
):
    """Main method for training the lasso model"""
    houses_df = load_train_dataset(input_filepath=input_filepath)

    # split the dataset
    X_train, X_test, y_train, y_test = split_dataset(
        train_df=houses_df,
        train_size=train_size,
        split_seed=split_seed
    )

    # start experiment tracking
    experiment = mlflow.set_experiment(experiment_name="houses_lasso_train")
    with mlflow.start_run(experiment_id=experiment.experiment_id):
        # create the training pipeline
        pipeline = create_lasso_pipeline(
            rare_threshold, X_train, alpha, model_seed
        )

        # fit the pipeline
        pipeline.fit(X_train, y_train)

        # track the experiment's transformations
        mlflow.log_param("rare_threshold", rare_threshold)
        mlflow.log_param("numeric_transformations", "norm, yj, impute_mean")
        mlflow.log_param("categorical_transformations", "replace_rare, ohe")
        mlflow.log_param("ordinals_transformations", "ordinal_encoding")
        # track model parameters and metrics
        mlflow.log_param('alpha', alpha)
        mlflow.log_param('model_random_seed', model_seed)


        # track the model in moflow
        track_mlflow_model(pipeline, f"lasso_{__version__}")
        model_uri = mlflow.get_artifact_uri(f"lasso_{__version__}")

        # evaluate the model and track the metrics
        mlflow.evaluate(
            model_uri,
            X_test.assign(y=y_test),
            targets="y",
            model_type="regressor",
            dataset_name="houses_test",
            evaluators=["default"]
        )

        # save the lasso to the models registry
        save_path = save_model(pipeline)
        _logger.info("Saved the lasso pipeline at %s", save_path)


def create_lasso_pipeline(rare_threshold, X_train, alpha, model_seed):
    """Create a pipeline for the lasso regression"""
    categoricals = X_train.columns.intersection(constants.CATEGORICAL_COLUMNS)
    numericals = X_train.columns.intersection(constants.NUMERICAL_COLUMNS)

    numeric_pipeline = Pipeline([
        ('impute_with_mean', SimpleImputer(strategy='mean')),
        ('scaling', StandardScaler()),
        ('yeo_johnson', PowerTransformer())
    ])

    # transformations to be applied to categorical features
    categoric_pipeline = Pipeline([
        ('replace_rare', RareCategoriesReplacer(rare_threshold)),
        ('one_hot_encoding', OneHotEncoder())
    ])

    # transformations on the response variable
    response_variable_pipeline = Pipeline([
        ('normalization', StandardScaler()),
        ('yeo_johnson', PowerTransformer())
    ])

    all_transformations = ColumnTransformer(
        transformers=[
            ('numeriric_transformations', numeric_pipeline, numericals),
            ('categoric_transformations', categoric_pipeline, categoricals),
            ('ordinals_encoding', __ordinal_encoder, constants.ORDINALS)
        ],
        remainder='passthrough'
    )

    pipeline = Pipeline(
        steps=[
            ('column_transformations', all_transformations),
            ('lasso_and_target_transform', TransformedTargetRegressor(
                regressor=Lasso(alpha=alpha, random_state=model_seed),
                transformer=response_variable_pipeline
            ))
        ]
    )
    return pipeline


def load_train_dataset(input_filepath=constants.DEFAULT_TRAIN_INPUT_PATH):
    """Load our dataset used for training"""
    return pd.read_csv(input_filepath)


def split_dataset(
    train_df: pd.DataFrame,
    train_size: float=constants.DEFAULT_TRAIN_SET_SIZE,
    split_seed: int=constants.DEFAULT_SPLIT_SEED
):
    """Split the dataset producing a training and test sets"""
    return train_test_split(
        train_df.drop([constants.TARGET_VARIABLE_NAME, 'Id'], axis=1),
        train_df[constants.TARGET_VARIABLE_NAME],
        train_size=train_size,
        random_state=split_seed
    )


def train(
    input_filepath: str=constants.DEFAULT_TRAIN_INPUT_PATH,
    train_size: float=constants.DEFAULT_TRAIN_SET_SIZE,
    split_seed: int=constants.DEFAULT_SPLIT_SEED,
    rare_threshold=constants.DEFAULT_RARE_CATEGORIES_DROP_THRESHOLD,
    alpha=constants.DEFAULT_LASSO_ALPHA,
    model_seed=constants.DEFAULT_MODEL_SEED
):
    """Train the lasso regression"""
    houses_df = load_train_dataset(input_filepath=input_filepath)

    # split the dataset
    X_train, _, y_train, _ = split_dataset(
        train_df=houses_df,
        train_size=train_size,
        split_seed=split_seed
    )

    pipeline = create_lasso_pipeline(rare_threshold, X_train, alpha, model_seed)
    pipeline.fit(X_train, y_train)
    save_model(pipeline)

    return pipeline


def save_model(pipeline) -> str:
    """A method to save the output path"""
    model_name = f"lasso_{__version__}"
    save_path = config.TRAINED_MODELS_DIR / f"{model_name}.pkl"
    joblib.dump(pipeline, save_path)
    return save_path


def track_mlflow_model(model, model_name):
    """Track the model in the mlflow model registry"""
    tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
    # Model registry does not work with file store
    if tracking_url_type_store != "file":
        # Register the model
        # There are other ways to use the Model Registry, which depends on the use case,
        # please refer to the doc for more information:
        # https://mlflow.org/docs/latest/model-registry.html#api-workflow
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path=f"lasso_{__version__}",
            registered_model_name=f"lasso_{__version__}"
        )
    else:
        mlflow.sklearn.log_model(sk_model=model, artifact_path=model_name)


if __name__ == "__main__":
    main()
