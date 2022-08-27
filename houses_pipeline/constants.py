"""Different constants used for the pipeline"""

YEAR_COLUMNS = ['YearBuilt', 'YearRemodAdd', 'GarageYrBlt']
INTERVAL_COLUMNS = ['BuiltTilSold', 'RemodTilSold', 'GarageBuildTilSold']
# LISTWISE_DELETION_COLUMNS = ['MasVnrArea', 'MasVnrType', 'Electrical']
DEFAULT_MISSING_THRESHOLD = 0.80

REDUNDANT_COLUMNS = [
    'Street', 'Utilities', 'LandSlope', 'Condition2', 'RoofMatl', 'BsmtCond',
    'Heating', 'CentralAir', 'Electrical', 'LowQualFinSF', 'BsmtHalfBath',
    'KitchenAbvGr', 'Functional', 'GarageQual', 'GarageCond', 'PavedDrive',
    '3SsnPorch', 'ScreenPorch', 'PoolArea', 'MiscVal',
    'Exterior2nd', 'GarageYrBlt'
]

ORDINALS = ["BsmtQual", "ExterQual", "ExterCond", "FireplaceQu", "KitchenQual"]
ORDINALS_ORDERING = ['Missing', 'Po', 'Fa', 'TA', 'Gd', 'Ex']

CATEGORICAL_COLUMNS = [
   'GarageQual', 'GarageCond', 'PoolQC',
  'BsmtCond', 'Alley', 'Fence','RoofStyle', 'MiscFeature',
  'Heating', 'CentralAir', 'Electrical',
  # 'BsmtHalfBath',
  # 'KitchenAbvGr',
  'Functional', 'PavedDrive',
  'Street', 'Utilities', 'LandSlope', 'Condition1', 'Condition2', 'RoofMatl',
  'MSZoning', 'LotShape', 'LandContour', 'LotConfig', 'Neighborhood',
  'Condition1', 'BldgType', 'HouseStyle', 'RoofStyle', 'Exterior1st',
  'Exterior2nd',
  'Foundation', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2', 'HeatingQC',
  'GarageType', 'GarageFinish', 'SaleType', 'SaleCondition',
  # "BsmtQual", "ExterQual", "ExterCond", "FireplaceQu", "KitchenQual",
  "MasVnrType"
]

NUMERICAL_COLUMNS = [
  'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', '1stFlrSF', '2ndFlrSF','GrLivArea',
  'BsmtFullBath', 'FullBath', 'HalfBath', 'BedroomAbvGr', 'TotRmsAbvGrd',
  'MiscVal',
  'GarageArea', 'WoodDeckSF', 'OpenPorchSF', 'EnclosedPorch', 'GarageCars',
  'MoSold', 'LotFrontage', 'LotArea', 'MSSubClass', 'WoodDeckSF', 'OpenPorchSF',
  'EnclosedPorch', 'MoSold', 'MasVnrArea', 'BsmtFinSF1', 'LowQualFinSF', '3SsnPorch', 'ScreenPorch'
]

# default params
DEFAULT_REDUNDANT_COLUMNS_THRESHOLD = 0.9
DEFAULT_NAN_COLUMNS_THRESHOLD = 0.9
DEFAULT_RARE_CATEGORIES_DROP_THRESHOLD = 0.1

DEFAULT_INPUT_PATH = "data/raw/train.csv"
DEFAULT_OUTPUT_PATH = "data/interim/train.csv"

# arguments helps
INPUT_PATH_HELP = "The path of the csv file to preprocess"
OUTPUT_PATH_HELP = "Where to store the processed path"
REDUNDANT_COLUMNS_HELP = """A threshold to use above which to drop drop nan columns"""
NAN_COLUMNS_THRESHOLD_HELP = """Drop if the column is mostly the same"""
RARE_CATEGORIES_DROP_THRESHOLD_HELP = "Replace rare categories"
VERBOSE_HELP = "Whether to print the steps of the pipeline"

DROP_COLUMNS = ['GarageYrBlt', 'YrSold', 'Exterior2nd', 'PoolQC']

TARGET_VARIABLE_NAME = "SalePrice"
