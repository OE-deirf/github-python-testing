# Simple code for testing

# venv
## with pip
- python3.10 -m venv .venv
- source .venv/bin/activate
- pip install -v -r requirements.txt/requirements_dev.txt

## with uv
- uv venv --python 3.10
- source .venv/bin/activate
- uv pip install -r requirements.txt/requirements_dev.txt

# GIT  init
- git init
- dvc init            # create .dvc/ dir
- git commit -m "DVC init"

# GIT commit
- git add <file>
- git commit -m "commit messgae"
- git push

# checkout
- git pull
- git checkout <branch>

# checkout only with old file version
- git checkout <branch> -- <file>

# pytest coverage
- pytest ./tests/ --cov

# with coverage tool:
- coverage run -m pytest
- coverage report -m

