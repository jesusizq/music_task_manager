# BMAT Task Manager

## Overview

This is BMAT backend API to manage tasks, such as CSV processing, etc.

The API is built using Flask and will run on a local server at: `http://localhost:5000/v1/<endpoint>`

The API will receive a POST request with a CSV file and will process it asynchronously using a docker container with a RabbitMQ broker.

## Environment variables

The following environment variables are required to run the app:

```sh
export FLASK_APP=run.py
export RABBITMQ_BROKER=127.0.0.1
export RABBITMQ_PORT=5672
export RABBITMQ_USER=bmat_admin
export RABBITMQ_PASSWORD=BM4AT_4dm1n
export RABBITMQ_QUEUE=task_queue
````

## Dependencies

Install dependencies (`poetry` >=1.5.0 needs to be [installed](https://python-poetry.org/docs/#installing-with-the-official-installer) on the system)

Depending on your IDE, you may need to configure the python interpreter to use the poetry environment (i.e. [PyCharm](https://www.jetbrains.com/help/pycharm/poetry.html))

If the previous step has not done it automatically, now you have to install dependencies:

```sh
poetry install
```

Activate `poetry environment`:

```sh
poetry shell
```

## Running the app

### 1) Launch the docker containers

To get started, you will need to move to the docker directory and run `docker-compose.yml` file with:

```sh
docker-compose -f up && docker-compose logs -f 
```

### 2) Run the app

```sh
poetry run flask run
```
Or alternatively:
```sh
poetry shell
flask run
```
