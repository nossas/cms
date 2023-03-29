FROM python:3.9

ARG DATABASE_URL
ARG DEFAULT_STORAGE_DSN
ARG DEBUG
ARG DOMAIN_ALIASES
ARG SECURE_SSL_REDIRECT

WORKDIR /app
COPY ./webproject /app
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput
CMD uwsgi --http=0.0.0.0:80 --module=backend.wsgi --honour-stdin
