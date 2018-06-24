# STANDARDLIB
import logging
import pandas as pd
from datetime import timedelta

# THRID-PARTY
from peewee import *

# LOCAL-APP
from .base import BaseModel, db, get_current_date_time, TableMaker


class SuperHot(BaseModel):
    name = CharField(unique=True)
    date = DateTimeField(null=False)

    def add_coin(name):
        try:
            kwargs = {'name': name, 'date': get_current_date_time()}
            SuperHot.create(**kwargs)
            print(f'{name} created.')  # TODO: Logging
        except IntegrityError:
            print(f'{name} already exists.')
            db.rollback()
            SuperHot.update_coin(name)

    def update_coin(name):
        try:
            kwargs = {'name': name, 'date': get_current_date_time()}
            query = SuperHot.update(**kwargs).where(SuperHot.name == name)
            query.execute()
            print(f'{name} updated.')  # TODO: LOGGING
        except SuperHot.DoesNotExist:
            kwargs = {'name': name, 'date': get_current_date_time()}
            SuperHot.add_coin(**kwargs)
            print(f'{name} doesnt exist')

    def query_all():
        query = SuperHot.select(SuperHot.name,
                                SuperHot.date).dicts()

        df = pd.DataFrame(list(query))
        df.set_index('date', inplace=True)
        return df

    def fetch_hot(hours=12, max_=5):
        query_time = get_current_date_time() - timedelta(hours=hours)
        query = SuperHot.select(SuperHot.name,
                                SuperHot.date,
                                ).where(SuperHot.date > query_time).dicts()
        df = pd.DataFrame(list(query))
        df.set_index('date', inplace=True)
        df.sort_index(inplace=True)
        return list(df.tail(max_)['name'])


SuperHotTables = TableMaker([SuperHot])
