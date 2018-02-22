web: gunicorn --access-logfile - --log-level debug --worker-class gevent wsgi:app
worker: celery -A app.celery worker --loglevel=info -P gevent
