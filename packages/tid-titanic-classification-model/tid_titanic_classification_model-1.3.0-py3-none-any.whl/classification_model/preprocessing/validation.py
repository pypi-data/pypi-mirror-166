import typing as t

import pandas as pd
from pydantic import BaseModel, Field, ValidationError

from classification_model.config.core import config
from classification_model.preprocessing.data_manager import pre_pipeline_preparation


def validate_input(
    input_data: pd.DataFrame,
) -> t.Tuple[pd.DataFrame, t.Optional[t.Dict]]:
    errors = None
    pre_processed = None
    try:
        pre_processed = pre_pipeline_preparation(input_data)
        pre_processed = pre_processed[config.model_config.features]
        MultipleTitanicDataInputs(inputs=pre_processed.to_dict(orient="records"))
    except ValidationError as error:
        errors = error.errors()

    return pre_processed, errors


class TitanicInputSchema(BaseModel):
    pclass: int
    sex: str
    age: float
    sibsp: int
    parch: int
    fare: float
    cabin: str
    embarked: str
    name: t.Optional[str]
    ticket: t.Optional[str]
    boat: t.Optional[t.Union[str, int]]
    body: t.Optional[int]
    home_dest: t.Optional[str] = Field(alias="home.dest")


class MultipleTitanicDataInputs(BaseModel):
    inputs: t.List[TitanicInputSchema]
