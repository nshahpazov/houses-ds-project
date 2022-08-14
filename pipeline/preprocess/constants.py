"""A module containing all the constants used in the preprocessing step"""

YEAR_COLUMNS = ['YearBuilt', 'YearRemodAdd', 'GarageYrBlt']
INTERVAL_COLUMNS = ['BuiltTilSold', 'RemodTilSold', 'GarageBuildTilSold']
YEAR_SOLD_COLUMN_NAME = 'YrSold'

ORDINALS = ["BsmtQual", "ExterQual", "ExterCond", "FireplaceQu", "KitchenQual"]
ORDINALS_ORDERING = ['Missing', 'Po', 'Fa', 'TA', 'Gd', 'Ex']

YEAR_COLUMNS = ['YearBuilt', 'YearRemodAdd', 'GarageYrBlt']
INTERVAL_COLUMNS = ['BuiltTilSold', 'RemodTilSold', 'GarageBuildTilSold']
YEAR_SOLD_COLUMN_NAME = 'YrSold'
YEAR_COLUMNS = ['YearRemodAdd']
YEAR_BUILT_COLUMN = 'YearBuilt'
COLUMNS_WITH_RARE_VALUES = ['Alley', 'PoolQC', 'Fence', 'MiscFeature']
LISTWISE_DELETION_COLUMNS = ['MasVnrArea', 'MasVnrType', 'Electrical']
DEFAULT_MISSING_THRESHOLD = 0.80

REDUNDANT_COLUMNS = [
    'Street', 'Utilities', 'LandSlope', 'Condition2', 'RoofMatl', 'BsmtCond',
    'Heating', 'CentralAir', 'Electrical', 'LowQualFinSF', 'BsmtHalfBath',
    'KitchenAbvGr', 'Functional', 'GarageQual', 'GarageCond', 'PavedDrive',
    '3SsnPorch', 'ScreenPorch', 'PoolArea', 'MiscVal',
    'Exterior2nd', 'GarageYrBlt'
]

CATEGORICAL_COLUMNS = [
  'MSZoning','LotShape', 'LandContour', 'LotConfig', 'Neighborhood',
  'Condition1', 'BldgType', 'HouseStyle', 'RoofStyle', 'Exterior1st',
  'Foundation', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2', 'HeatingQC',
  'GarageType', 'GarageFinish', 'GarageCars', 'SaleType', 'SaleCondition',
  "BsmtQual", "ExterQual", "ExterCond", "FireplaceQu", "KitchenQual"
]
