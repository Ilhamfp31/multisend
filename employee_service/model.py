from playhouse.shortcuts import model_to_dict, dict_to_model
from peewee import *
from datetime import datetime

db = SqliteDatabase('employee_service/data.db')

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


class Employee(BaseModel):
    user_id = IntegerField()
    first_name = CharField()
    last_name = CharField()
    bank_name = CharField()
    bank_account_number = IntegerField()
    phone_number = IntegerField()

    class Meta:
        db_table = 'employee'