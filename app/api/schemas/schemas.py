from app import ma
from app.models import Task
from marshmallow import (
    fields,
    INCLUDE,
)


class PaginationSchema(ma.Schema):
    page = ma.Int(missing=1)
    page_size = ma.Int(missing=50)


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_relationships = True

    message = ma.Str()


class TaskUpdateSchema(ma.Schema):
    class Meta:
        unknown = INCLUDE

    status = ma.Str(required=True)
