import json
import structlog
import toml
from copy import deepcopy
from collections import ChainMap

from .constants import CLEAN_JSON_CONFIG_PATH, CONFIGURATION_PATH

# TODO: THIS SHOULD NOT init exchange and token info.
# TODO: THIS should update the gunbot config, read clean.json, and read configuration toml files
# TODO: ad debug structlog


class GunBotConfigInterface:

    def __init__(self):
        self.config = self._load_clean()

        self._check_configuration_toml_folder()
        self.toml_config = self._load_tomls()

    def update_config_from_toml(self):
        new_config = dict(ChainMap(self.toml_config, self.config))
        self.config = new_config

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

    def dump_json(self):
        data = self.config
        return json.dumps(data, indent=4)

    def _write_clean_configuration_tomls(self):
        print('writing toml files')
        data = self.config
        for section, data in data.items():
            if section != 'pairs':
                file_path = (CONFIGURATION_PATH/section).with_suffix('.toml')
                if not file_path.exists():
                    with open(file_path, 'w') as f:
                        print(f'Writing {file_path}')
                        f.write(toml.dumps(data))

    def _check_configuration_toml_folder(self):
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
            self._write_clean_configuration_tomls()
            self._check_configuration_toml_folder()
