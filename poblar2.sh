#!/bin/bash

pg_dump dbsigepro -U sigepro > sigepro.sql
dropdb dbsigepro
psql -U sigepro -d dbsigepro -f sigepro.sql
python manage.py makemigrations
python manage.py migrate

