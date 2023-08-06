import pandas as pd

from classification_model.config.core import config
from classification_model.preprocessing.features import ExtractLetterTransformer


def test_temporal_variable_transformes(sample_input_data):

    X_test, y_test = sample_input_data

    transformer = ExtractLetterTransformer(variables=config.model_config.cabin)
    X_test = transformer.transform(X_test)

    assert X_test["cabin"].iat[0] == "?"

    assert X_test["sex"].iat[1] == "female"
    assert X_test.shape[0] == len(y_test)

    assert isinstance(X_test, pd.DataFrame)
    assert isinstance(y_test, pd.Series)
