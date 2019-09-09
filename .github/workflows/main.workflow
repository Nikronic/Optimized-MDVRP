name: CI

on: [push]

jobs:
  build:

    runs-on: ubuntu-latest
    
    steps:
    - name: Setup Python
      uses: actions/setup-python@v1
      with:
        python-version: '3.6'
        architecture: 'x64'
    - name: Install Dependencies
      run: |
        pip freeze > requirements.txt
        pip install -r requirements.txt
      shell: bash
    - name: GitHub Action for pytest
      uses: cclauss/GitHub-Action-for-pytest@0.0.2
    - name: Run Pytest tests
      run: python -m pytest
      shell: bash

# workflow "Build and Test" {
#   on = "push"
#   resolves = [
#     "Test",
#   ]
# }

# action "Build" {
#   uses = "jefftriplett/python-actions@master"
#   args = "pip install -r requirements.txt"
# }

# action "Lint" {
#   uses = "jefftriplett/python-actions@master"
#   args = "black --check"
#   needs = ["Build"]
# }

# action "Test" {
#   uses = "jefftriplett/python-actions@master"
#   args = "pytest"
#   needs = ["Lint"]
# }


# workflow "on push" {
#   on = "push"
#   resolves = ["GitHub Action for pytest"]
# }

# action "GitHub Action for pytest" {
#   uses = "cclauss/GitHub-Action-for-pytest@master"
#   args = "pytest -h"
# }
