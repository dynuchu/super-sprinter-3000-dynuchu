from connectdatabase import ConnectDatabase
from peewee import *

class BaseModel(Model):
    class Meta:
        database = ConnectDatabase.db

class UserStoryManager(BaseModel):
    story_title = CharField()
    user_story = TextField()
    acceptance_criteria = TextField()
    business_value = IntegerField()
    estimation = FloatField()
    status = CharField()



