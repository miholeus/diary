setup:
	pip install -r requirements/base.txt
	python manage.py migrate
	python manage.py collectstatic --noinput

run:
	python manage.py runserver

.PHONY: setup
