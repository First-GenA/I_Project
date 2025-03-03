#!/usr/bin/bash
# Exit on error
set -o errexit

# install requirements
pip install -r requirements.txt

# convert static asset files
python manage.py collectstatic --no-input
# apply migrations
python manage.py migrate
