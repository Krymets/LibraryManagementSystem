web: gunicorn project.wsgi --log-file=- -w 3 --timeout 25
release: python manage.py migrate