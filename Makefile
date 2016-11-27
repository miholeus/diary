setup:
	pip install -r requirements/base.txt
	python manage.py migrate
	python manage.py collectstatic --noinput

.PHONY: setup
