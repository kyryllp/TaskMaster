import mongoengine
from datetime import datetime


class Todo(mongoengine.Document):
    content = mongoengine.StringField(required=True)
    date_created = mongoengine.DateTimeField(default=datetime.utcnow)
