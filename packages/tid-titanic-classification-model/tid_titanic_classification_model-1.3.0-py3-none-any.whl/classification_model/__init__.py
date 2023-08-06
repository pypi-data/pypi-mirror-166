from classification_model.config.core import PACKAGE_ROOT

with open(PACKAGE_ROOT / "VERSION") as file:
    __version__ = file.read()
