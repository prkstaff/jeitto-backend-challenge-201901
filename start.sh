#!/bin/sh

# apply db models
flask db upgrade

gunicorn -w 4 -b 127.0.0.1:8080 app:app
