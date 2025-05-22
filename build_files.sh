#!/bin/bash

echo "Installing dependencies..."
python3.9 -m pip install --no-cache-dir -r requirements-prod.txt

echo "Cleaning up Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type f -name "*.pyd" -delete
rm -f db.sqlite3 db.sqlite3.backup

echo "Setting up static files..."
mkdir -p staticfiles_build/static

echo "Collecting static files..."
python3.9 manage.py collectstatic --noinput

echo "Optimizing deployment size..."
rm -rf tests/
rm -rf docs/
rm -rf .git/
rm -rf node_modules/
rm -rf media/

echo "Build completed!"
