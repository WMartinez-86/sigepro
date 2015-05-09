#!/bin/bash

dropdb dbsigepro
createdb dbsigepro
python manage.py makemigrations
python manage.py migrate
python poblar.py
