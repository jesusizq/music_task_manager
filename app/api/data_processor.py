from . import data_processor_api as api
from flask import jsonify


@api.route("/example", methods=["GET"])
def get_examples():
    return jsonify(
        [
            {"example": "example1"},
            {"example": "example2"},
        ]
    )


@api.route("/example", methods=["POST"])
def example():
    return jsonify({"result": "success"})
