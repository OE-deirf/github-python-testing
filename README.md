# Simple code for testing

# venv
## with pip
- python3.10 -m venv .venv
- source .venv/bin/activate
- pip install -v -r requirements.txt

## with uv
- uv venv --python 3.10
- source .venv/bin/activate
- uv pip install -r requirements.txt

# GIT  init
- git init
- git add .
- git commit -m "init"

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

