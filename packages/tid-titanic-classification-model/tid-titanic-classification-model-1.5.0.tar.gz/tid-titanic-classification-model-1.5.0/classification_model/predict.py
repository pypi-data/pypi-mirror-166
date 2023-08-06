import typing as t

import pandas as pd

from classification_model import __version__ as _version
from classification_model.config.core import config
from classification_model.preprocessing.data_manager import load_pipeline
from classification_model.preprocessing.validation import validate_input

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.joblib"

titanic_pipe = load_pipeline(file_name=pipeline_file_name)


def make_prediction(input_data: t.Union[pd.DataFrame, dict]) -> dict:
    """Make predictions

    Args:
        input_data (t.Union[pd.DataFrame, dict]): Input data from either Pandas Dataframe
        or Dictionary

    Returns:
        dict: Dictionary containing the prediction
    """
    data = pd.DataFrame(input_data)
    data, errors = validate_input(data)
    results = {"predictions": None, "version": _version, "errors": errors}
    if not errors:
        predictions = titanic_pipe.predict(data)
        results = {"predictions": list(predictions), "version": _version, "errors": errors}
    return results
