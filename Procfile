web: gunicorn --access-logfile - --log-level debug --worker-class gevent wsgi:app
worker: celery -A app.my_celery worker --loglevel=info --without-gossip --without-mingle --without-heartbeat -P gevent
