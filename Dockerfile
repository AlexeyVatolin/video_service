FROM python:3.10-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc ffmpeg \
    && pip install poetry==1.2.2

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry export --without-hashes -f requirements.txt --dev \
    |  poetry run pip install -r /dev/stdin 

# RUN poetry install --no-interaction

COPY . /app/