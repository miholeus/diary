# Diary

Diary project based on Django framework

Features:

1. Analytics in personal trainings
2. Progress in body development
3. Intellectual suggestion on physics improvement

## Installation

    $ pip install -r requirements/base.txt
    $ python manage.py migrate
    $ python manage.py runserver

Add your settings in `config/settings/local.py`

Set `DEBUG=False`, add `ALLOWED_HOSTS`
Then run:

    $ python manage.py collectstatic --noinput

Or you can simply run:

    $ make setup

## Run project

Run command

    $ make run

## Current status

In development
