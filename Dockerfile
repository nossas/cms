# Build static files
FROM node:18-alpine AS node-builder

WORKDIR /app

COPY . .

WORKDIR /app/tailwind

RUN npm ci || npm install

RUN npm run page:build
RUN npm run admin:build


# Python runtime - Debian Bookworm
FROM python:3.10-slim-bookworm

# Port used by this container to serve HTTP.
EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        cargo \
        libssl-dev \
        libffi-dev \
        sox \
        ffmpeg \
        libcairo2 \
        libcairo2-dev \
        python3-dev \
        git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade packaging tools
RUN python -m pip install --upgrade pip setuptools wheel

# Install application dependencies
RUN pip install \
    uwsgi \
    django-storages \
    boto3 \
    django-prometheus

# Install project requirements
COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

# Application directory
WORKDIR /app

# Copy project including generated frontend/static assets
COPY --from=node-builder /app /app

# Generate Django static files
RUN python manage.py collectstatic \
    --noinput \
    --clear \
    -i tailwindcss

# Check traefik + etcd configs for running domains
ENV ENABLE_CHECK_TRAEFIK=True

CMD ["uwsgi", "--ini", "/app/wsgi.ini"]
