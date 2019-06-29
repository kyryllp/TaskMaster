import mongoengine


class User(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    surname = mongoengine.StringField(required=True)
    username = mongoengine.StringField(required=True)
    password = mongoengine.StringField(required=True)

    todo_ids = mongoengine.ListField()