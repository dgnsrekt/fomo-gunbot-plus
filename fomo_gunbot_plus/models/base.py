from datetime import datetime

from peewee import PostgresqlDatabase, Model

db = PostgresqlDatabase('fomo_gunbot_plus_db')


def get_current_date_time():
    return datetime.utcnow()


class BaseModel(Model):

    class Meta:
        database = db
