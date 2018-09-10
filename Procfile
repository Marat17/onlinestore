web: gunicorn onlinestore.wsgi --log-file -
worker: celery worker --app=onlinestore.tasks.app