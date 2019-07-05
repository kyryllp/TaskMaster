import mongoengine


def global_init():
    mongoengine.register_connection(alias='core', db='simple_todo', host='db')
