# THIRD PARTY IMPORTS
import toml
import structlog

# LOCAL IMPORTS
from .constants import CONFIGFILE_PATH


class Configuration:
    def __init__(self):
        self.logger = structlog.get_logger()

        self.general = dict()
        self.load_config()

    def load_config(self):
        if not CONFIGFILE_PATH.exists():
            CONFIGFILE_PATH.touch()
            self.logger.info('Config.toml not found.')
            self.write_blank()

        with open(CONFIGFILE_PATH, 'r') as f:
            data = toml.loads(f.read())

        self.general = data['GENERAL']
        self.logger.info('Config.toml loaded.')

    def write_blank(self):
        general = dict()
        general['IGNORE_PAIRS'] = ['USDT', 'TUSD']
        general['FORCE_BAGS'] = []
        general['EXCHANGE'] = 'binance'
        general['RESET_CHART_DATA'] = False
        general['MAX_BAGS_TIL_DUMP'] = 5
        general['DUMP_BAGS_OVER_24H_OLD'] = False

        data = dict()
        data['GENERAL'] = general

        with open(CONFIGFILE_PATH, 'w') as f:
            f.write(toml.dumps(data))
            self.logger.info('Config.toml written.')
