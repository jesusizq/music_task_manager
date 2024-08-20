# BMAT Task Manager

## Overview

This is BMAT backend API to manage tasks, such as CSV processing, etc.

The API is built using Flask and will run on a local server at: `http://localhost:5000/v1/<endpoint>`

The API will receive a POST request with a CSV file and will process it asynchronously using a docker container with a RabbitMQ broker.

## Environment variables

The following environment variables are required to run the app:

```sh
export FLASK_APP=run.py \
export FLASK_CONFIG=testing \
export LOCAL_STORAGE_PATH=../local_storage \
export TEST_DATABASE_URL=mysql://root:BM4AT_4dm1n@127.0.0.1:3306/bmat \
export RABBITMQ_BROKER=127.0.0.1 \
export RABBITMQ_PORT=5672 \
export RABBITMQ_USER=bmat_admin \
export RABBITMQ_PASSWORD=BM4AT_4dm1n \
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

Now, if necessary, use the following command to deploy whatever is needed in the database:

```sh
flask deploy
```

## Faking data

To fake data, you can run the following script:
    
```sh
python3 song_faker.py
```

## Running the app

### 1) Launch the docker containers

To get started, you will need to move to the docker directory and run `docker-compose.yml` file with:

```sh
docker-compose up -d && docker-compose logs -f 
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

## Modifying the database

Once you have modified your model, you must apply the changes in the database. Make sure to have the last version before migrating.
```sh
flask db upgrade # Optional: to have the last version
flask db migrate -m <message>
flask db upgrade
```