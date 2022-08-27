"""Train a lasso regression"""
# generally used modules
# import joblib
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

# model tracking
import mlflow
import mlflow.sklearn

# internal modules
from houses_pipeline import constants

from houses_pipeline.transformers import RareCategoriesReplacer

__ordinal_encoder = OrdinalEncoder(
    categories=[constants.ORDINALS_ORDERING] * len(constants.ORDINALS),
    handle_unknown='use_encoded_value',
    unknown_value=-1
)


@click.command()
@click.argument(
    'input_filepath',
    type=click.Path(exists=True),
    default=constants.DEFAULT_INPUT_PATH
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
    default=0.05,
    help="Regularization model seed"
)
@click.option(
    '--rare_threshold',
    'rare_threshold',
    required=False,
    default=0.05,
    help="Rare Threshold"
)
def main(input_filepath, alpha, model_seed, rare_threshold):
    """Main method for training the lasso model"""
    train_df = pd.read_csv(input_filepath)


    # to set some additional notes in mlflow tracking use:
    # mlflow.note.content

    X_train = train_df.drop(constants.TARGET_VARIABLE_NAME, axis=1)
    y_train = train_df[constants.TARGET_VARIABLE_NAME]

    categoricals = X_train.columns & constants.CATEGORICAL_COLUMNS
    numericals = X_train.columns & constants.NUMERICAL_COLUMNS

    with mlflow.start_run():
        # transformations to apply to the numerical predictors
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

        # track the experiment's transformations
        mlflow.log_param("rare_threshold", rare_threshold)
        mlflow.log_param("numeric_transformations", "norm, yj, impute_mean")
        mlflow.log_param("categorical_transformations", "replace_rare, ohe")
        mlflow.log_param("ordinals_transformations", "ordinal_encoding")

        pipeline = Pipeline(
            steps=[
                ('column_transformations', all_transformations),
                ('lasso_and_target_transform', TransformedTargetRegressor(
                    regressor=Lasso(alpha=alpha, random_state=model_seed),
                    transformer=response_variable_pipeline
                ))
            ]
        )

        # fit the pipeline
        pipeline.fit(X_train, y_train)

        # track model parameters and metrics
        mlflow.log_param('alpha', alpha)
        mlflow.log_param('model_random_seed', model_seed)

        mlflow.sklearn.log_model(
            sk_model=pipeline,
            artifact_path="lasso_model",
            code_paths=[
                "notebooks/03-ns-modelling.ipynb",
                "pipeline/modelling/train_lasso.py"
            ],
            registered_model_name="LassoRegression"
        )


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
