from flask import Flask, jsonify


def create_app():
    app = Flask(__name__)

    @app.route("/example", methods=["GET"])
    def get_examples():
        return jsonify(
            [
                {"example": "example1"},
                {"example": "example2"},
            ]
        )

    @app.route("/example", methods=["POST"])
    def example():
        return jsonify({"result": "success"})

    return app
