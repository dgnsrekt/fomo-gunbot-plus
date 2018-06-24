# SYSTEM IMPORTS
import json
import os
import structlog
import toml
from collections import ChainMap, OrderedDict
from copy import deepcopy
from datetime import datetime

# THIRD PARTY IMPORTS
import pandas as pd
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

# LOCAL IMPORTS
from .constants import (CLEAN_JSON_CONFIG_PATH,
                        CONFIGURATION_PATH,
                        CONFIG_JS_PATH,
                        GUNBOT_PATH,
                        DELISTED_PATH,
                        BASEPATH)

from .states import ColdState, HotState


class GunBotConfigInterface:

    def __init__(self):
        self.logger = structlog.get_logger()
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

    def update_pairs(self, hotpairs, coldpairs, exchange):
        self.update_config_from_toml()

        h = HotState(hotpairs)
        c = ColdState(coldpairs)

        h_pairs = h.prepare_config()
        c_pairs = c.prepare_config()

        hotcold = {**h_pairs, **c_pairs}

        pairs = dict()
        pairs[exchange] = hotcold

        self.config['pairs'] = pairs

    def update_pairs_from_live(self):
        live = self._load_live()
        self.config['pairs'] = live['pairs']

    def check_for_change(self):
        live = self._load_live()

        diff = self.config == live
        self.logger.info(f'Compare: {diff}')
        return diff

    def write_to_gunbot_config(self):
        # TODO Compare current file dictions to what is being written if no changes do nothing.
        if not self.check_for_change():
            data = self._dump_json()
            with open(CONFIG_JS_PATH, 'w') as f:
                f.write(data)
            self.logger.info(f'Wrote to {CONFIG_JS_PATH}')
        else:
            self.logger.info('No changes needed.')

    def _load_live(self):
        with open(CONFIG_JS_PATH, 'r') as f:
            live_json = json.loads(f.read())
        return live_json

    def _load_clean(self):
        with open(CLEAN_JSON_CONFIG_PATH, 'r') as f:
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
        self.logger.info('writing toml files')
        data = self.config
        for section, data in data.items():
            if 'pairs' not in section:
                file_path = (CONFIGURATION_PATH/section).with_suffix('.toml')
                if not file_path.exists():
                    with open(file_path, 'w') as f:
                        self.logger.info(f'Writing {file_path}')
                        f.write(toml.dumps(data))

    def check_configuration_toml_folder(self):
        self.logger.info('Checking toml files.')
        try:
            assert (CONFIGURATION_PATH / 'bot.toml').exists(), 'Missing bot.toml'
            assert (CONFIGURATION_PATH / 'exchanges.toml').exists(), 'Missing exchange.toml'
            assert (CONFIGURATION_PATH / 'imap_listener.toml').exists(), 'Missing imap_listener.toml'
            assert (CONFIGURATION_PATH / 'strategies.toml').exists(), 'Missing strategies.toml'
            assert (CONFIGURATION_PATH / 'version.toml').exists(), 'Missing version.toml'
            assert (CONFIGURATION_PATH / 'ws.toml').exists(), 'Missing ws.toml'
            self.logger.info('All toml files found.')

        except AssertionError as e:
            self.logger.info(e)
            self.write_clean_configuration_tomls()
            self.check_configuration_toml_folder()


def state_file_reader(path_):
    try:
        with open(path_, 'r') as f:
            data = json.loads(f.read())
        return data
    except json.decoder.JSONDecodeError as e:
        print(path_)
        print(e)
        return None


def parse_name_from_path(path_):
    return path_.name.split('-')[2]


def parse_datetime(path_):
    mtime = path_.stat().st_mtime
    return datetime.utcfromtimestamp(mtime)


class GunBotStateInterface:

    def __init__(self):
        self.logger = structlog.get_logger()

        self.state_file_data = self._extract()
        self.estimated_value = 0
        self.raw_bags = []
        self.real_bags = []
        self.all_pairs = []

        if self.state_file_data:
            self._transform()

    def _extract(self):
        trade_state_paths = sorted(GUNBOT_PATH.glob('*-state.json'),
                                   key=os.path.getmtime, reverse=True)

        temp = []
        for jsonpath in trade_state_paths:
            data = state_file_reader(jsonpath)
            time = parse_datetime(jsonpath)
            name = parse_name_from_path(jsonpath)

            data['name'] = name
            data['time'] = time

            if data != None:
                temp.append(data)

        if len(temp) > 0:
            return temp
        else:
            return None  # TODO: Catch this None

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
            self.estimated_value = current_df['btc_value'].sum() + list(current_df['btc'])[0]
        except IndexError:
            self.estimated_value = 0

        self.real_bags = list(current_df[current_df['btc_value'] > 0.0001]['name'])
        self.all_pairs = list(balances.keys())

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
