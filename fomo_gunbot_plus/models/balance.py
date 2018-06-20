# STANDARDLIB
import logging
import pandas as pd
from datetime import timedelta

# THRID-PARTY
from peewee import *

# LOCAL-APP
from .base import BaseModel, db, get_current_date_time


class Balance(BaseModel):
    btc = DecimalField(null=False)
    date = DateTimeField(null=False)

    def add(amount):
        kwargs = {'btc': amount}
        kwargs['date'] = get_current_date_time()
        Balance.create(**kwargs)
        print(f'{kwargs} written.')  # TODO: Logging

    def pull(time_frame='5T'):
        query = Balance.select(Balance.btc,
                               Balance.date).dicts()

        df = pd.DataFrame(list(query))
        df.set_index('date', inplace=True)
        df = df.resample(time_frame).last()
        return df


def create_balance_table():
    db.create_tables([Balance])
    logging.info('Telegram Table Created')


def drop_balance_table():
    db.drop_tables([Balance])
    logging.info('Telegram Table Dropped')


def clean_balance_table():
    drop_balance_table()
    create_balance_table()
