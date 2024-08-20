import os
from flask import request, jsonify, send_file
from app import db, logger
from . import data_processor_api as api
from rabbit.utils import send_job
from app.models import Task, TaskStatus, TaskType
from apifairy import other_responses
import time
import uuid
from flask import current_app


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

    if int(request.headers["Content-Length"]) > 5 * 1024 * 1024:
        logger.error(f"File too large. Max size: 5MB")
        return jsonify({"error": "File too large"}), 400

    try:
        logger.info(f"File received: {file.filename}")

        filename = f"raw_{uuid.uuid4()}.csv"
        raw_storage = os.path.join(current_app.config.get("STORAGE_PATH"), "raw_data")
        abs_raw_storage = os.path.abspath(raw_storage)

        if not os.path.exists(abs_raw_storage):
            os.makedirs(abs_raw_storage)

        file_path = os.path.join(abs_raw_storage, filename)

        logger.info(f"Uploading file to {file_path}...")
        file.save(file_path)
        time.sleep(5)  # Simulate processing time
        logger.info(f"File uploaded successfully")

        task = Task(
            task_type=TaskType.CSV,
            status=TaskStatus.RECEIVED,
            file_input_path=file_path,
        )
        db.session.add(task)
        db.session.commit()

        # Publish message
        rabbit_queue = current_app.config.get("RABBITMQ_QUEUE")
        logger.info(f"Sending task [{task.id}] to Rabbit queue [{rabbit_queue}]")
        send_job(
            {
                "task_id": task.id,
                "type": task.task_type.name,
                "status": task.status.name,
                "file_path": file_path,
            },
            rabbit_queue,
        )

        return jsonify({"task_id": task.id}), 202
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@api.route("/notify", methods=["POST"])
@other_responses({404: "Task not found"})
def notify_task_completion():
    data = request.get_json()
    task_id = data.get("task_id")
    status = data.get("status")
    file_output_path = data.get("file_output_path")

    if not task_id or not status or not file_output_path:
        return jsonify({"error": "Invalid data"}), 400

    task = Task.query.get_or_404(task_id)

    if task.status == TaskStatus.PROCESSING:
        task.status = (
            TaskStatus.DONE if status == TaskStatus.DONE.name else TaskStatus.FAILED
        )
        task.file_output_path = file_output_path
        db.session.add(task)
        db.session.commit()
        return jsonify({"task_id": task.id}), 200
    else:
        return jsonify({"error": "Task not processing"}), 400


@api.route("/download/<task_id>", methods=["GET"])
@other_responses({404: "Task not found"})
def download_csv(task_id):
    task = Task.query.get_or_404(task_id)

    if task.status == TaskStatus.PROCESSING or task.status == TaskStatus.RECEIVED:
        return jsonify({"error": "Task processing"}), 400
    elif task.status == TaskStatus.FAILED:
        return jsonify({"error": "Task failed"}), 400
    elif task.status == TaskStatus.CANCELLED:
        return jsonify({"error": "Task cancelled"}), 400
    elif task.status == TaskStatus.DONE:
        logger.info(f"Preparing file to download {task.file_output_path}")
        time.sleep(5)  # Simulate preparation time
        logger.info(f"File ready to download")
        return send_file(task.file_output_path, as_attachment=True), 200
    else:
        return jsonify({"error": "Unknown status"}), 400
