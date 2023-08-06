from pathlib import Path
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

NAME = "tid-titanic-classification-model"
AUTHORS = "Edcalderin"
AUTHOR_EMAIL = "edcm.erick@gmail.com"
DESCRIPTION = "Example Titanic classification model package"
README = "README.md"
REQUIRES_PYTHON = ">=3.7"

HOMEPAGE = "https://github.com/edcalderin/deployment-titanic-classification-model"

PACKAGE_ROOT = Path(__file__).resolve().parent
PACKAGE_DIR = PACKAGE_ROOT/'classification_model'
REQUIREMENTS_DIR = PACKAGE_ROOT/'requirements'

about ={}
with open(PACKAGE_DIR/'VERSION') as file:
    about['__version__'] = file.read()

def list_requirements():
    with open(REQUIREMENTS_DIR/'requirements.txt') as file:
        return file.read().splitlines()

setup(
        name=NAME,
        version=about['__version__'],
        package_data={'classification_model': ['VERSION']},
        packages=find_packages(),
        description=DESCRIPTION,
        long_description=long_description,
        long_description_content_type="text/markdown",
        url=HOMEPAGE,
        author=AUTHORS,
        author_email=AUTHOR_EMAIL,
        license="MIT",
        python_requires=REQUIRES_PYTHON,
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
        ],
        install_requires=list_requirements()
)