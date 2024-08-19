# BMAT Task Manager

## Overview

This is BMAT backend API to manage tasks, such as CSV processing, etc.

The API is built using Flask, Blueprints, and will run on a local server at: `http://localhost:5000/v1/<endpoint>`

### Dependencies

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

In order to run the app, use the next command:

```sh
poetry run flask run
```
Or alternatively:
```sh
poetry shell
flask run
```
