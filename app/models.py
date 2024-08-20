import uuid
from . import db
from enum import IntEnum, auto


class TaskStatus(IntEnum):
    RECEIVED = auto()
    PROCESSING = auto()
    DONE = auto()
    FAILED = auto()
    CANCELLED = auto()


class TaskType(IntEnum):
    CSV = auto()


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_type = db.Column(db.Enum(TaskType), nullable=False)
    status = db.Column(db.Enum(TaskStatus), nullable=False)
    file_input_path = db.Column(db.String(255), nullable=False)
    file_output_path = db.Column(db.String(255), nullable=True)

    def __init__(self, task_type, status, file_input_path):
        self.task_type = task_type
        self.status = status
        self.file_input_path = file_input_path
