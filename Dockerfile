FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    pkg-config \
    libmariadb-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry install

COPY . /app

EXPOSE 5000