#!/usr/bin/env bash

# Cài gói
pip install -r requirements.txt

# Migrate database
python manage.py migrate

# Collect static
python manage.py collectstatic --noinput
