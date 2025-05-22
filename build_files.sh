echo "Installing dependencies..."
pip install --no-cache-dir -r requirements-prod.txt

echo "Removing development files..."
rm -rf __pycache__
rm -rf *.pyc
rm -f db.sqlite3
rm -f db.sqlite3.backup

echo "Creating static files directory..."
mkdir -p staticfiles_build/static

echo "Collecting static files..."
python -m manage.py collectstatic --noinput

echo "Build completed!"
