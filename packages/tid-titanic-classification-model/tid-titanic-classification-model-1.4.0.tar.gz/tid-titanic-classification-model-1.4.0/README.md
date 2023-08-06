# Titanic Classifier

## Build and distribute package
Only Windows.
Go to https://packaging.python.org/en/latest/tutorials/packaging-projects/ to see instructions in Linux.

1. (First time) `py -m pip install --upgrade pip`
2. (First time) `py -m pip install --upgrade build`
3. `py -m build`
4. (First time) `py -m pip install --upgrade twine`
5.
    - For testpypi:  
        `py -m twine upload --repository testpypi dist/*`

    - For Pypi:  
        `py -m twine upload dist/*`