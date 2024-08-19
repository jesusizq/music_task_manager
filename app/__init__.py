from flask import Flask
from apifairy import APIFairy

apifairy = APIFairy()


def create_app():
    app = Flask(__name__)

    from .api import (
        data_processor_api,
    )

    app.register_blueprint(data_processor_api, url_prefix="/v1/data_processor")

    return app
