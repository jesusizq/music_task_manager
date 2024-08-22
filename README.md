# BMAT Task Manager [![BMAT](https://www.bmat.com/wp-content/uploads/2021/01/cropped-bmat-logo-32x32.png)](https://www.bmat.com/es/)

## Overview

Backend API that runs at: `http://localhost:5000/v1/<endpoint>`.

Its role is to manage and assign tasks to associated services. It does it **asynchronously** via a RabbitMQ broker and a MySQL database.

Another service will receive a task from the Task Manager via rabbit, process the data, and then notify it back when the task is done.

_**Disclaimer**: The `BMAT_task_manager/external` directory contains rabbit and logger libraries. They are there so the Dockerfile can copy them to the container. In a real-world scenario, they should be published and installed via Poetry, as all the other dependencies._

## Environment variables

The following environment variables are required to run the app:

```sh
FLASK_APP=run.py
FLASK_CONFIG=testing
STORAGE_PATH
TEST_DATABASE_URL
RABBITMQ_BROKER
RABBITMQ_PASSWORD
RABBITMQ_PORT
RABBITMQ_USER
RABBITMQ_QUEUE
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

Now, if necessary, use the following command to deploy whatever is needed in the database:

```sh
flask deploy
```

## Faking data

To fake a raw CSV data, you can run the following script to store a raw CSV at `utils/csv_files`:
    
```sh
python3 song_faker.py
```

## Running the app

### 1) Launch the docker containers

To get started, move to the docker directory and run `docker-compose.yml` inside:

```sh
cd docker
docker-compose up -d && docker-compose logs -f
```
### 2) Run the app

Make sure you have updated the database before running the app:

```sh
poetry run flask db upgrade # Optional: update the database (if necessary)
poetry run flask run
```

Or, alternatively, if you have an `docker/.env` file ready (that way the docker-compose has access to the variables), you can execute the following script:

```sh
bash ./docker_entry_point.sh --env-file ./docker/.env
```

If you just want to upgrade the database while applying the environment variables, you can run:
```sh
bash ./docker_entry_point.sh --env-file ./docker/.env --skip-run
```

## Modifying the database

Once you have modified your database models, you must apply the changes in the database. Make sure to have the last version before migrating.
```sh
flask db upgrade # Optional: to have the last version
flask db migrate -m <message>
flask db upgrade
```

## Dockerizing the app

To dockerize the app, you can run the following command:

```sh
docker build -t bmat-task-manager .
```

Alternatively, you can use the `docker-compose.yml` file (at the root of the project) to build the image and run the container with the app, rabbit and mysql services:

```sh
docker-compose up --build -d && docker-compose logs -f
```

_**Disclaimer**_: `docker-compose.yml` is not yet working correctly. Sometimes it
does not connect the `app` service with the `db` service, due to the `TEST_DATABASE_URL` environment variable.