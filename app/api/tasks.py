import os
from flask import url_for, jsonify
from app import db
from . import tasks_api as api
from app.api.schemas.schemas import TaskSchema, TaskUpdateSchema, PaginationSchema
from app.models import Task, TaskStatus
from apifairy import response, other_responses, body, arguments
from flask import current_app


raw_storage = os.path.join(current_app.config.get("STORAGE_PATH"), "raw_data")


@api.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@api.route("")
@arguments(PaginationSchema)
def get_tasks(pagination_input):
    page = pagination_input["page"]
    page_size = pagination_input["page_size"]
    pagination = Task.query.order_by(Task.time_stamp.desc()).paginate(
        page, per_page=page_size, error_out=False
    )
    tasks = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for("Tasks.get_tasks", page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for("Tasks.get_tasks", page=page + 1)
    return {
        "tasks": tasks,
        "prev_url": prev,
        "next_url": next,
        "count": len(tasks),
    }, 200


@api.route("/<task_id>", methods=["GET"])
@response(TaskSchema, 200)
@other_responses({404: "Task not found."})
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return task


@api.route("/<task_id>", methods=["DELETE"])
@response(TaskSchema, 200)
@other_responses({404: "Task not found."})
def cancel_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = TaskStatus.CANCELLED
    db.session.add(task)
    db.session.commit()
    return task


@api.route("/status/<task_id>", methods=["PUT"])
@body(TaskUpdateSchema)
@response(TaskSchema, 200)
@other_responses({404: "Task not found", 400: "Incorrect status"})
def edit_task_status(task_parameters, task_id):
    task = Task.query.get_or_404(task_id)
    status = task_parameters["status"]
    if status not in TaskStatus.__members__:
        return {"error": "Incorrect status"}, 400
    task.status = TaskStatus[status]
    db.session.add(task)
    db.session.commit()


@api.route("/status/<task_id>", methods=["GET"])
@other_responses({404: "Task not found"})
def get_status(task_id):
    task = Task.query.get_or_404(task_id)
    if task.status == TaskStatus.DONE:
        return (
            jsonify(
                {
                    "status": task.status.name,
                    "download_link": f"http://localhost:5000/v1/data_processor/download/{task_id}",
                }
            ),
            200,
        )

    return jsonify({"status": task.status.name}), 200
