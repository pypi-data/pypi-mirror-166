from feature_engine.encoding import OneHotEncoder, RareLabelEncoder
from feature_engine.imputation import (
    AddMissingIndicator,
    CategoricalImputer,
    MeanMedianImputer,
)
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from classification_model.config.core import config
from classification_model.preprocessing.features import ExtractLetterTransformer

# set up the pipeline
titanic_pipe = Pipeline(
    [
        # ===== IMPUTATION =====
        # impute categorical variables with string 'missing'
        (
            "categorical_imputation",
            CategoricalImputer(variables=config.model_config.categorical_variables),
        ),
        # add missing indicator to numerical variables
        (
            "missing_indicator",
            AddMissingIndicator(variables=config.model_config.numerical_variables),
        ),
        # impute numerical variables with the median
        (
            "median_imputation",
            MeanMedianImputer(variables=config.model_config.numerical_variables),
        ),
        # Extract first letter from cabin
        (
            "extract_letter",
            ExtractLetterTransformer(variables=config.model_config.cabin),
        ),
        # == CATEGORICAL ENCODING ======
        # remove categories present in less than 5% of the observations (0.05)
        # group them in one category called 'Rare'
        (
            "rare_label_encoder",
            RareLabelEncoder(variables=config.model_config.categorical_variables),
        ),
        # encode categorical variables using one hot encoding into k-1 variables
        (
            "categorical_encoder",
            OneHotEncoder(
                variables=config.model_config.categorical_variables, drop_last=True
            ),
        ),
        # scale using standardization
        ("scaler", StandardScaler()),
        # logistic regression (use C=0.0005 and random_state=0)
        ("Logit", LogisticRegression(C=0.0005, random_state=config.model_config.seed)),
    ]
)
