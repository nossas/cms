# Build staticfiles
FROM node:18-alpine AS node-builder

WORKDIR /app

# TODO: Copiar apenas arquivos para o build do node
COPY . .

WORKDIR /app/tailwind

RUN npm i

RUN npm run page:build

RUN npm run admin:build

# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:slim-buster

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system packages required by Django CMS and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
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

# Install the application server.
RUN pip install uwsgi django-storages boto3 django-prometheus

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Copy the source code of the project into the container.
COPY --from=node-builder /app ./

# Install the project requirements.
# Os arquivos do projeto foram copiados em sua totalidade no node-builder e por esse motivo
# essa linha precisa ser executada após trazer os arquivos do node-builder pra esse stage
# em Python
RUN pip install -r org_nossas/requirements.txt

RUN python manage.py collectstatic --noinput --clear -i tailwindcss

# Runtime command that executes when "docker run" is called.

# Check traefik + etcd configs to running domains
ENV ENABLE_CHECK_TRAEFIK=True

CMD ["uwsgi", "--ini", "/app/wsgi.ini"]
