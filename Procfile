web: daphne project.asgi:application --port $PORT --bind 0.0.0.0 -v2
celery: celery -A project worker -l info
channels: python manage.py runworker -v2
release: ./release.sh
