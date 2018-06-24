# STANDARDLIB
import pandas as pd
from datetime import timedelta

# THRID-PARTY
import structlog
from peewee import *

# LOCAL-APP
from .base import BaseModel, db, get_current_date_time, TableMaker


class Status(BaseModel):
    balance = DecimalField(null=False)
    positions = BigIntegerField()

    date = DateTimeField(null=False)

    def update(bal, pos):
        kwargs = dict()
        kwargs['balance'] = bal
        kwargs['positions'] = pos
        kwargs['date'] = get_current_date_time()
        Status.create(**kwargs)

    def fetch(time_frame='5T'):
        query = Status.select(Status.balance,
                              Status.positions,
                              Status.date).dicts()

        df = pd.DataFrame(list(query))
        df.set_index('date', inplace=True)
        df = df.resample(time_frame).last()
        return df


ViewTables = TableMaker([Status])
