from playhouse.shortcuts import model_to_dict, dict_to_model
from peewee import *
from datetime import datetime
from authentication_broker.util import generate_token


db = SqliteDatabase('authentication_broker/data.db')


class BaseModel(Model):
    updated_at = DateTimeField(default=datetime.now)
    created_at = DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)

    def serialize(self):
        return model_to_dict(self, backrefs=True, recurse=False)

    class Meta:
        database = db


class User(BaseModel):
    email = CharField()
    password = CharField()
    access_token = CharField(default=generate_token)

    def serialize(self):
        return model_to_dict(self, only=[User.id, User.email, User.access_token, User.updated_at, User.created_at])

    class Meta:
        db_table = 'user'
