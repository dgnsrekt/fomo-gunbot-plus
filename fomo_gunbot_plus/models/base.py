from datetime import datetime

from peewee import PostgresqlDatabase, Model
import structlog

db = PostgresqlDatabase('fomo_gunbot_plus_db')


def get_current_date_time():
    return datetime.utcnow()


class BaseModel(Model):

    class Meta:
        database = db


class TableMaker:

    def __init__(self, tables):
        self.tables = tables
        self.logger = structlog.get_logger()

    def create(self):
        db.create_tables(self.tables)
        self.logger.info(f'{self.tables} Tables Created')

    def drop(self):
        logger = structlog.get_logger()
        db.drop_tables(self.tables)
        self.logger.info(f'{self.tables} Tables Dropped')

    def clean(self):
        self.drop()
        self.create()
