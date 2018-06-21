import json
import structlog
import toml
import os
from datetime import datetime
from copy import deepcopy
from collections import ChainMap, OrderedDict
import pandas as pd

from .constants import (CLEAN_JSON_CONFIG_PATH,
                        CONFIGURATION_PATH,
                        CONFIG_JS_PATH,
                        GUNBOT_PATH,
                        DELISTED_PATH,
                        BASEPATH)

# TODO: THIS SHOULD NOT init exchange and token info.
# TODO: THIS should update the gunbot config, read clean.json, and read configuration toml files
# TODO: ad debug structlog


class GunBotConfigInterface:

    def __init__(self):
        self.config = self._load_clean()

        self.check_configuration_toml_folder()
        self.toml_config = self._load_tomls()

    def update_config_from_toml(self):
        new_config = dict(ChainMap(self.toml_config, self.config))
        order_config = OrderedDict()

        order_config['version'] = new_config['version']
        order_config['pairs'] = new_config['pairs']
        order_config['strategies'] = new_config['strategies']
        order_config['exchanges'] = new_config['exchanges']
        order_config['bot'] = new_config['bot']
        order_config['ws'] = new_config['ws']
        order_config['imap_listener'] = new_config['imap_listener']

        self.config = order_config

    def write_to_gunbot_config(self):
        data = self._dump_json()
        with open(CONFIG_JS_PATH, 'w') as f:
            f.write(data)
        print('Wrote to configuration file.')

    def _load_clean(self):
        with open(CLEAN_JSON_CONFIG_PATH) as f:
            clean_json = json.loads(f.read())
        return clean_json

    def _load_tomls(self):
        paths_ = CONFIGURATION_PATH.glob('*.toml')
        files_ = [p for p in paths_ if p.name != 'states.toml']

        data = dict()
        for f in files_:
            with open(f, 'r') as e:
                data[f.stem] = toml.loads(e.read())
        return data

    def _dump_json(self):
        data = self.config
        return json.dumps(data, indent=4)

    def write_clean_configuration_tomls(self):
        print('writing toml files')
        data = self.config
        for section, data in data.items():
            if 'pairs' not in section:
                file_path = (CONFIGURATION_PATH/section).with_suffix('.toml')
                if not file_path.exists():
                    with open(file_path, 'w') as f:
                        print(f'Writing {file_path}')
                        f.write(toml.dumps(data))

    def check_configuration_toml_folder(self):
        print('Checking toml files.')
        try:
            assert (CONFIGURATION_PATH / 'bot.toml').exists(), 'Missing bot.toml'
            assert (CONFIGURATION_PATH / 'exchanges.toml').exists(), 'Missing exchange.toml'
            assert (CONFIGURATION_PATH / 'imap_listener.toml').exists(), 'Missing imap_listener.toml'
            assert (CONFIGURATION_PATH / 'strategies.toml').exists(), 'Missing strategies.toml'
            assert (CONFIGURATION_PATH / 'version.toml').exists(), 'Missing version.toml'
            assert (CONFIGURATION_PATH / 'ws.toml').exists(), 'Missing ws.toml'
            print('All toml files found.')

        except AssertionError as e:
            print(e)
            self.write_clean_configuration_tomls()
            self.check_configuration_toml_folder()


class GunBotStateInterface:

    def __init__(self):
        self.state_file_data = self._extract()
        self.estimated_value = 0
        self.raw_bags = []
        self.real_bags = []
        self.all_pairs = []

        if self.state_file_data:
            self._transform()

    @staticmethod
    def state_file_reader(path_):
        with open(path_, 'r') as f:
            return json.loads(f.read())

    @staticmethod
    def parse_name_from_path(path_):
        return path_.name.split('-')[2]

    @staticmethod
    def parse_datetime(path_):
        mtime = path_.stat().st_mtime
        return datetime.utcfromtimestamp(mtime)

    def _extract(self):
        trade_state_paths = sorted(GUNBOT_PATH.glob('*-state.json'),
                                   key=os.path.getmtime, reverse=True)

        temp = []
        for jsonpath in trade_state_paths:
            data = GunBotStateInterface.state_file_reader(jsonpath)
            time = GunBotStateInterface.parse_datetime(jsonpath)
            name = GunBotStateInterface.parse_name_from_path(jsonpath)

            data['name'] = name
            data['time'] = time

            temp.append(data)

        if len(temp) > 0:
            return temp
        else:
            return None

    def _transform(self):
        balances = self.state_file_data[0]['balancesdata']
        positive_balances = [bal for bal in balances if balances[bal]['available'] > 0]

        state_df = pd.DataFrame(self.state_file_data)
        columns = ['name', 'Bid', 'Ask', 'quoteBalance', 'baseBalance', 'time']
        current_df = state_df[columns]
        current_df = current_df[current_df['name'].isin(positive_balances)]
        current_df['price'] = (current_df['Bid'] + current_df['Ask']) / 2
        current_df['btc_value'] = current_df['price'] * current_df['quoteBalance']
        current_df.columns = ['name', 'bid', 'ask', 'balance', 'btc', 'time', 'price', 'btc_value']

        self.raw_bags = positive_balances
        try:
            self.estimated_value = current_df['btc_value'].sum() + current_df['btc'][0]
        except IndexError:
            self.estimated_value = 0

        self.real_bags = list(current_df[current_df['btc_value'] > 0.0001]['name'])
        self.all_pairs = list(balances.keys())

    @property
    def fetch_bags(self):
        if len(self.real_bags) > 0:
            return self.real_bags
        elif len(self.raw_bags) > 0:
            return self.raw_bags
        else:
            return []

    def load(self):
        pass

    def __repr__(self):
        repr_ = f'Estimated Value: {self.estimated_value}\n'
        repr_ += f'Real Bags: {self.real_bags}\n'
        repr_ += f'Raw Bags: {self.raw_bags}\n'
        repr_ += f'All Pairs: {self.all_pairs}\n'
        return repr_
