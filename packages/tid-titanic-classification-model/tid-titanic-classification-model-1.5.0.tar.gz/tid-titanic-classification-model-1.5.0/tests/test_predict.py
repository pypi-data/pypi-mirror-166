from typing import Tuple

import numpy as np
import pandas as pd

from classification_model.predict import make_prediction


def test_predict(sample_input_data: Tuple[pd.DataFrame, pd.Series]):
    X_test, _ = sample_input_data

    results = make_prediction(input_data=X_test)
    predictions = results.get("predictions")

    assert results.get("errors") is None
    assert isinstance(predictions[0], np.int64)
    assert len(predictions) == X_test.shape[0]
