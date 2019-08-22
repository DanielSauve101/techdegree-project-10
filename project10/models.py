from peewee import *

import config

DATABASE = SqliteDatabase('tasks.sqlite')

class Todo(Model):
    name = CharField()
    completed = BooleanField(default=False)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect(reuse_if_open=True)
    DATABASE.create_tables([Todo], safe=True)
    DATABASE.close()
