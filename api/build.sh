#!/bin/bash
python3.9 -m pip install -r api/requirements.txt
python3.9 manage.py collectstatic --noinput
rm -rf __pycache__/
rm -rf */__pycache__/
rm -rf */*/__pycache__/
rm -rf .pytest_cache/
rm -rf .coverage
rm -rf htmlcov/
rm -rf .tox/
rm -rf dist/
rm -rf build/
rm -rf *.egg-info/
