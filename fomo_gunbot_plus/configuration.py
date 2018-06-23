import toml

from .constants import CONFIGFILE_PATH


class Configuration:
    def __init__(self):
        self.general = dict()
        self.load_config()

    def load_config(self):
        if not CONFIGFILE_PATH.exists():
            CONFIGFILE_PATH.touch()
            self.write_blank()

        with open(CONFIGFILE_PATH, 'r') as f:
            data = toml.loads(f.read())

        self.general = data['GENERAL']

    def write_blank(self):
        general = dict()
        general['IGNORE_PAIRS'] = ['USDT', 'TUSD']
        general['EXCHANGE'] = 'binance'

        data = dict()
        data['GENERAL'] = general

        with open(CONFIGFILE_PATH, 'w') as f:
            f.write(toml.dumps(data))
