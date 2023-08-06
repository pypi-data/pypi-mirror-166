from pathlib import Path
from typing import Optional, Sequence

from pydantic import BaseModel
from strictyaml import YAML, load

import classification_model

# Project directories
PACKAGE_ROOT = Path(classification_model.__file__).resolve().parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yml"
TRAINED_MODELS_DIR = PACKAGE_ROOT / "trained_models"


class AppConfig(BaseModel):
    package_name: str
    pipeline_save_file: str


class ModelConfig(BaseModel):
    target: str
    numerical_variables: Sequence[str]
    categorical_variables: Sequence[str]
    cabin: Sequence[str]
    features: Sequence[str]
    unused_fields: Sequence[str]
    path_dataset: str
    test_size: float
    seed: int


class Config(BaseModel):
    app_config: AppConfig
    model_config: ModelConfig


def find_config_file() -> Path:
    """Locate the config file"""
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    else:
        raise Exception(f"Config file not found at {CONFIG_FILE_PATH!r}")


def load_config_from_yaml(config_path: Optional[Path] = None) -> YAML:
    try:
        if not config_path:
            config_path = find_config_file()

        with open(config_path) as file:
            config = load(file.read()).data
            return config
    except FileNotFoundError:
        raise OSError(f"Did not find config file at path {config_path}")


def create_and_validate_config(
    parsed_config: YAML = None,
) -> Config:
    if parsed_config is None:
        parsed_config = load_config_from_yaml()

    config = Config(
        app_config=AppConfig(**parsed_config), model_config=ModelConfig(**parsed_config)
    )
    return config


config = create_and_validate_config()
