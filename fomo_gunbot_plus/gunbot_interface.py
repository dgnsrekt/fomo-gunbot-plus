import json
import structlog
import toml
from datetime import datetime
from copy import deepcopy
from collections import ChainMap
from collections import ChainMap, OrderedDict
import pandas as pd

from .constants import CLEAN_JSON_CONFIG_PATH, CONFIGURATION_PATH, CONFIG_JS_PATH, GUNBOT_PATH, DELISTED_PATH
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

#
# class GunBotStateInterface:
#
#     def __init__(self):
#         self.state_json_files = list(GUNBOT_PATH.glob('*-state.json'))
#         self.state_json_df = self._load_df()
#         self.avaliable_state_files = self._get_avaliable_state_file()
#
#         self.non_zero_state_dataframe = self._get_non_zero_state_files()
#
#     def _load_df(self):
#
#         temp = []
#         if len(self.state_json_files) > 0:
#             package = dict()
#             for _file in self.state_json_files:
#                 name = _file.name.split('-')[2]
#                 file_path = _file
#                 mod_date = datetime.utcfromtimestamp(_file.stat().st_mtime)
#                 package['name'] = name
#                 package['file_path'] = file_path
#                 package['mod_date'] = mod_date
#                 temp.append(package)
#
#             df = pd.DataFrame(temp)
#             df.sort_values(by='mod_date', inplace=True)
#             return df
#         else:
#             return None
#
#     def _get_avaliable_state_file(self):
#         if len(self.state_json_df) > 0:
#             r = list(self.state_json_df['name'])
#             r.sort()
#             return r
#         else:
#             return list()
#
#     @property
#     def latest_state_file(self):
#         if len(self.state_json_df) > 0:
#             return self.state_json_df.tail(1)['file_path'].values[0]
#         else:
#             None
#
#     @classmethod
#     def get_delisted(cls):
#         with open(DELISTED_PATH, 'r') as f:
#             dlisted = toml.loads(f.read())
#         return dlisted
#
#     def _get_non_zero_state_files(self):
#         with open(self.latest_state_file, 'r') as f:
#             last_updated_json = json.loads(f.read())
#
#         latest_balance_data = last_updated_json['balancesdata']
#         latest_non_zero_balances = [
#             coin for coin in latest_balance_data if latest_balance_data[coin]['available']]
#
#         delisted = GunBotStateInterface.get_delisted()
#         latest_non_zero_balances = [
#             coin for coin in latest_non_zero_balances if coin not in delisted]
#
#         latest_non_zero_balances.sort()
#
#         non_zero_state_files = [
#             state_file for state_file in self.avaliable_state_files if state_file in latest_non_zero_balances]
#         non_zero_state_files.sort()
#         df = self.state_json_df
#         df = df[df['name'].isin(non_zero_state_files)]
#         print(df)
#         return df
#
#     def get_bags(self):
#         files_to_search = list(self.non_zero_state_dataframe['file_path'])
#         print(files_to_search)
#
#     def get_balance(self):
#         pass
