#!/bin/sh

# Initialize database 
# This will do nothing by default if the db exists.
python3 init.py

# Run gunicorn
/usr/local/bin/gunicorn \
    --bind 0.0.0.0:8080 workshops_api.app:app
    -u nobody -g nogroup

