set PIPENV_VENV_IN_PROJECT=true
pipenv --python 3.9
if exist Pipfile (
    pipenv sync
)