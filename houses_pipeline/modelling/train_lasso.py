"""Train a lasso regression"""
# generally used modules
# import joblib
from urllib.parse import urlparse
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


__ordinal_encoder = OrdinalEncoder(
    categories=[constants.ORDINALS_ORDERING] * len(constants.ORDINALS),
    handle_unknown='use_encoded_value',
    unknown_value=-1
)


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
    default=0.05,
    help="Regularization parameter of the lasso regression"
)
@click.option(
    '--model_seed',
    'model_seed',
    required=False,
    default=1,
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
    '--rare_threshold',
    'rare_threshold',
    required=False,
    default=0.05,
    help="Rare Threshold"
)
def main(input_filepath, alpha, model_seed, split_seed, rare_threshold):
    """Main method for training the lasso model"""

    houses_df = pd.read_csv(input_filepath)

    X_train, X_test, y_train, y_test = train_test_split(
        houses_df.drop([constants.TARGET_VARIABLE_NAME, 'Id'], axis=1),
        houses_df[constants.TARGET_VARIABLE_NAME],
        train_size=0.8,
        random_state=split_seed
    )

    # to set some additional notes in mlflow tracking use:
    # mlflow.note.content

    # start experiment tracking
    experiment = mlflow.set_experiment(experiment_name="houses_lasso_train")
    with mlflow.start_run(experiment_id=experiment.experiment_id):
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

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        # Model registry does not work with file store
        if tracking_url_type_store != "file":

            # Register the model
            # There are other ways to use the Model Registry, which depends on the use case,
            # please refer to the doc for more information:
            # https://mlflow.org/docs/latest/model-registry.html#api-workflow
            mlflow.sklearn.log_model(
                sk_model=pipeline,
                artifact_path=f"lasso_{__version__}",
                registered_model_name=f"lasso_{__version__}"
            )
        else:
            mlflow.sklearn.log_model(
                sk_model=pipeline,
                artifact_path=f"lasso_{__version__}"
            )

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

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
