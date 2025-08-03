from marshmallow import Schema, fields, validate
from app.models import TaskStatus
from marshmallow_enum import EnumField 

class RegisterSchema(Schema):
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    phone = fields.Str(required=True, validate=validate.Length(equal=10))
    email = fields.Email(required=True)
    dob = fields.Str(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    description = fields.Str(allow_none=True)
    status = EnumField(TaskStatus, by_value=True)

class TaskUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=255))
    description = fields.Str(allow_none=True)
    status = fields.Str(validate=validate.OneOf([status.value for status in TaskStatus]))
