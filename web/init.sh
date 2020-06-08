#!/bin/sh
rm api/migrations/00*.py
rm test.db
rm *.db
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
python run_init.py