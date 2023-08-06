import re
from typing import List

import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from classification_model import __version__ as _version
from classification_model.config.core import TRAINED_MODELS_DIR, config


def load_dataset() -> pd.DataFrame:
    data = pd.read_csv(config.model_config.path_dataset)
    return pre_pipeline_preparation(data)


def _load_raw_dataset() -> pd.DataFrame:
    return pd.read_csv(config.model_config.path_dataset)


def pre_pipeline_preparation(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Prepipeline preparation

    Args:
        dataframe (pd.DataFrame): Pandas dataframe

    Returns:
        pd.DataFrame: Dataframe preprocessed
    """
    data = dataframe.replace("?", np.nan)

    data["title"] = data["name"].apply(get_title)

    data["fare"] = data["fare"].astype("float")
    data["age"] = data["age"].astype("float")
    data.drop(labels=config.model_config.unused_fields, axis=1, inplace=True)

    return data


def get_title(passenger: str) -> str:
    line = passenger
    if re.search("Mrs", line):
        return "Mrs"
    elif re.search("Mr", line):
        return "Mr"
    elif re.search("Miss", line):
        return "Miss"
    elif re.search("Master", line):
        return "Master"
    else:
        return "Other"


def save_pipeline(pipeline: Pipeline) -> None:
    pipeline_name = f"{config.app_config.pipeline_save_file}{_version}.joblib"

    remove_old_pipelines(files_to_keep=[pipeline_name])

    path = TRAINED_MODELS_DIR / pipeline_name

    joblib.dump(pipeline, path)


def remove_old_pipelines(files_to_keep: List[str]) -> None:
    do_not_delete = files_to_keep + ["__init__.py"]
    for file in TRAINED_MODELS_DIR.iterdir():
        if file not in do_not_delete:
            file.unlink()


def load_pipeline(file_name: str) -> Pipeline:
    path = f"{TRAINED_MODELS_DIR}/{file_name}"
    return joblib.load(path)
