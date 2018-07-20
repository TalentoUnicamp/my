web: daphne project.asgi:application
worker: celery -A project worker -l info
release: ./release.sh
