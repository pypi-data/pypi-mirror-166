from typing import Dict, List, Tuple, Union

import pandas as pd
import pytest
from sklearn.model_selection import train_test_split

from classification_model.config.core import config
from classification_model.preprocessing.data_manager import _load_raw_dataset


@pytest.fixture
def sample_input_data() -> Tuple[pd.DataFrame, pd.Series]:
    data = _load_raw_dataset()

    _, X_test, _, y_test = train_test_split(
        data.drop(config.model_config.target, axis=1),  # predictors
        data[config.model_config.target],  # target
        test_size=config.model_config.test_size,  # percentage of obs in test set
        random_state=config.model_config.seed,
    )  # seed to ensure reproducibility

    return X_test, y_test


@pytest.fixture
def get_titles() -> List[str]:
    return [
        "Mrs. Show",
        "Calvin Mr. Jhon",
        "The Miss. Claudia",
        "Unknown",
        "Master of puppets",
    ]
