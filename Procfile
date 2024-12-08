web: gunicorn bloomerz.wsgi
worker: celery -A bloomerz --loglevel=info
beat: celery -A bloomerz --loglevel=info
