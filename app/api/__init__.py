from flask import Blueprint
from flask_cors import CORS

data_processor_api = Blueprint("DataProcessor", __name__)
CORS(data_processor_api)
tasks_api = Blueprint("Tasks", __name__)
CORS(tasks_api)

from . import data_processor, tasks
