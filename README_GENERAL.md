# A microservices environment example

The project is a **microservices environment**. It's composed of backend environment to manage and assign tasks to associated services in an **asynchronous** way.

The connected service should take an input CSV file and process it:

- **Input CSV file**: “Song”, “Date”, “Number of Plays”. There will be many records for each song within each day. Input is not sorted.
- **Output CSV file**: “Song”, “Date, “Total Number of Plays for Date”. Output must be sorted ASC.

| Input Data                  | Output Data                 |
| --------------------------- | --------------------------- |
| `Song,Date,Number of Plays` | `Song,Date,Number of Plays` |
| Umbrella,2020-01-02,200     | In The End,2020-01-01,1500  |
| Umbrella,2020-01-01,100     | In The End,2020-01-02,500   |
| In The End,2020-01-01,500   | Umbrella,2020-01-01,150     |
| Umbrella,2020-01-01,50      | Umbrella,2020-01-02,250     |
| In The End,2020-01-01,1000  |
| Umbrella,2020-01-02,50      |
| In The End,2020-01-02,500   |

## Overview

This file contains the general information about the project. For more detailed information about each service, please refer to their respective `README.md` files.

The directory structure is as follows:

- `BMAT_task_manager`: backend API to manage and assign tasks asynchronously to associated services.
- `BMAT_data_processor`: service to process data, such as CSV files.
- `rabbit`: a common library to manage the rabbit connection and queues.
- `logger`: a common library to manage logs in the same way for every service.
- `local_storage`: a simulated cloud storage space to store CSV files.

### BMAT Task Manager

Backend API that runs at: `http://localhost:5000/v1/<endpoint>`.

Its role is to manage and assign tasks to associated services. It does it **asynchronously** via a RabbitMQ broker and a MySQL database.

_BMAT Data Processor_ will receive a task from the Task Manager via RabbitMQ, process the data, and then notify it back when the task is done.

The project includes:

- **Flask** framework to build the app
  - **Blueprints** to organize the app
  - **SQLAlchemy** ORM to manage the database
  - **Alembic** to manage the database migrations (Flask-Migrate)
- **Poetry** to manage the python dependencies
- **git** to manage the version control
- A `Dockerfile` to dockerize the app
- A `docker-compose.yml` to run the dockerized app along with a RabbitMQ broker and a MySQL database
- A `docker/docker-compose.yml` with RabbitMQ broker and a MySQL docker services, so you can **manually** run the app.
- An `.env` file to manage the environment variables (ignored by .gitignore)
- A `README.md` file with detailed information

Overall, a **robust and scalable solution** to manage tasks, ready to be deployed in a production environment, such as AWS, GCP, etc.

_**Disclaimer**: The `BMAT_task_manager/external` directory contains rabbit and logger libraries. They are there so the Dockerfile can copy them to the container. In a real-world scenario, they should be published and installed via Poetry, as all the other dependencies._

### BMAT Data Processor

A simple service to process CSV files with built-in Python libraries.

It asynchronously receives tasks via RabbitMQ broker, processes the data, and then notifies the Task Manager service when the task is done, making use of the Task Manager API.

The project includes:

- **Poetry** to manage the python dependencies
- **git** to manage the version control
- A `Dockerfile` to dockerize the app
- A `docker-compose.yml` file to run the app
- An `.env` file to manage the environment variables (ignored by .gitignore)
- A `README.md` file with detailed information

_**Disclaimer**: The `BMAT_data_processor/external` directory contains rabbit and logger libraries. They are there so the Dockerfile can copy them to the container. In a real-world scenario, they should be published and installed via Poetry, as all the other dependencies._

### Local Storage directory

A simulated cloud storage space to store CSV files. If deleted, the app will create it again.

Contains:

- `local_storage/raw_data`: the Task Manager will simulate cloud upload by saving the raw CSV files here.
- `local_storage/processed_data`: the Data Processor will save the processed CSV files here, simulating to save them in the cloud.

## Dependencies

You will need to install **Poetry** and **Docker** to run the project. Poetry will take care of the Python dependencies, while Docker will manage the containers.

## How to make it work

As we are simulating a microservices environment, we will need to run **BMAT_task_manager** and **BMAT_data_processor** services as detailed in their respective README files.

The general steps are:

- **POST** to `http://localhost:5000/v1/data_processor/upload` to upload a raw CSV file (same format as described in assignment)
- **GET** to `http://localhost:5000/v1/tasks/status/{task_id}` to check the task status
- **GET** to `http://localhost:5000/v1/data_processor/download/{task_id}` to download the processed CSV file when the task is done

To make your life easier, you can make use of the next `BMAT_task_manager/utils` scripts:

- `fake_songs.py` script to fake some data. It will create a raw CSV file with 1000 songs and save it in the `BMAT_task_manager/utils/csv_files` directory.
- `file_uploader.py` script to upload a file to the API and download it at `BMAT_task_manager/utils/csv_files` directory when the processing is done.

### Limitations

I encourage you to manually run both apps.

`BMAT_task_manager/docker-compose.yml` is not yet working correctly. Sometimes it
does not connect the `app` service with the `db` service, due to the `TEST_DATABASE_URL` environment variable.

Same with the `BMAT_data_processor/docker-compose.yml` file and the `rabbit` service.

## TO DO

- [ ] Add tests with coverage
- [ ] Add authentication to the API
- [ ] Add CI/CD pipelines
- [ ] Add more documentation
- [ ] Further check docker


## License

**Author**: Jesús Izquierdo Cubas

- [LinkedIn](https://www.linkedin.com/in/jesus-izquierdo-cubas/)
- Email: jesus.izquierdocubas@gmail.com

This project is intended for demonstration purposes only, specifically to showcase my skills and experience as a software engineer for potential employment opportunities. It is not to be used, distributed, or reproduced in any way, and is solely for review and evaluation by potential employers.
