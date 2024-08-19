from flask import Flask
from apifairy import APIFairy


apifairy = APIFairy()


def create_app(config_name):
    print("config_name", config_name)
    app = Flask(__name__)
    app.config.from_object(config_name)

    from .api import (
        data_processor_api,
    )

    app.register_blueprint(data_processor_api, url_prefix="/v1/data_processor")

    return app
