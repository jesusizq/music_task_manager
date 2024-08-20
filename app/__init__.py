import os
import tempfile
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_caching import Cache
from apifairy import APIFairy
from logger.Logger import Logger, LogLevel

apifairy = APIFairy()
db = SQLAlchemy()
ma = Marshmallow()
logger = Logger(LogLevel.INFO)
cache = Cache(
    config={
        "CACHE_TYPE": "FileSystemCache",
        "CACHE_DIR": os.path.join(tempfile.gettempdir(), "cache"),
    }
)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)

    apifairy.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)

    from app import models
    from .api import (
        data_processor_api,
        tasks_api,
    )

    app.register_blueprint(data_processor_api, url_prefix="/v1/data_processor")
    app.register_blueprint(tasks_api, url_prefix="/v1/tasks")

    return app
