#!/bin/sh

# apply db models
flask db upgrade

gunicorn -w 4 -b 0.0.0.0:8080 app:app
