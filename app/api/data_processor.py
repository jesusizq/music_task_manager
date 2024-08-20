import os
from flask import request, jsonify
from . import data_processor_api as api
from rabbit import rabbitmq_client
from app.models import Task, TaskStatus, TaskType
import uuid
import time

RABBITMQ_HOST = os.environ.get("RABBITMQ_BROKER", "localhost")
RABBITMQ_PORT = os.environ.get("RABBITMQ_PORT", 5672)
RABBITMQ_QUEUE = os.environ.get("RABBITMQ_QUEUE", "task_queue")
rabbit_client = rabbitmq_client.RabbitMQClient(
    host=RABBITMQ_HOST, port=RABBITMQ_PORT, queue=RABBITMQ_QUEUE
)

LOCAL_STORAGE_PATH = os.environ.get("LOCAL_STORAGE_PATH", "../../../local_storage")
raw_storage = os.path.join(LOCAL_STORAGE_PATH, "raw_data")
processed_storage = os.path.join(LOCAL_STORAGE_PATH, "processed_data")


@api.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@api.route("/upload", methods=["POST"])
def upload_csv():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    task_id = str(uuid.uuid4())
    filename = f"raw_{task_id}.csv"

    # Save file (simulate processing time)
    file_path = os.path.join(raw_storage, filename)
    file.save(file_path)
    time.sleep(5)

    # Create a new task and save it in database
    task = Task(
        task_type=TaskType.CSV, status=TaskStatus.PROCESSING, file_input_path=file_path
    )

    # Publish message
    message = {"task_id": task_id, "file_content": file.read().decode("utf-8")}
    rabbit_client.publish(message)

    return jsonify({"task_id": task_id}), 202


@api.route("/status/<task_id>", methods=["GET"])
def get_status(task_id):
    # TODO: Implement download logic
    return (
        jsonify(
            {
                "download_link": f"http://localhost:5000/v1/data_processor/download/{task_id}"
            }
        ),
        200,
    )


@api.route("/download/<task_id>", methods=["GET"])
def download_csv(task_id):
    # TODO: Implement download logic
    return jsonify({"message": "File ready for download"}), 200
