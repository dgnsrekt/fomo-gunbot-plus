# SYSTEM IMPORTS
from time import sleep

# THIRD PARTY IMPORTS
from fomo_superfilter.interface import BinanceDataFrameCreator
from fomo_superfilter.superfilter import SuperFilter
import structlog

# LOCAL IMPORTS
from .gunbot_interface import GunBotConfigInterface, GunBotStateInterface
from .configuration import Configuration
from .models.superhot import SuperHot, create_superhot_table
from .models.balance import Balance, create_balance_table, clean_balance_table


class Core:

    logger = structlog.get_logger()

    @classmethod
    def filter_hot(cls):
        cls.logger.info('Searching for hot coins...')
        config = Configuration()
        ignore_pairs = config.general['IGNORE_PAIRS']
        cls.logger.info(f'Ignoring pairs: {ignore_pairs}')

        binance_data = BinanceDataFrameCreator.prepare_dataframes()
        binance_btc = binance_data['BTC']
        binance_hot = SuperFilter.filter(binance_btc)
        binance_hot = [hot.split('BTC')[0] for hot in binance_hot]

        binance_names = list(binance_btc.index)
        binance_names = [name.split('BTC')[0] for name in binance_names]
        binance_names.sort()

        if not SuperHot.table_exists():
            create_superhot_table()

        for hot in binance_hot:
            if hot not in ignore_pairs:
                SuperHot.add_coin(hot)
                cls.logger.info(f'Superfilter found {hot}.')

    @classmethod
    def filter_cold(cls):
        cls.logger.info('Fetching bags...')
        GBSI = GunBotStateInterface()

        bags = GBSI.fetch_bags

        if not Balance.table_exists():
            create_balance_table()

        # clean_balance_table() #TODO: add a config option to reset chart, also it will backup old charts

        Balance.add(GBSI.estimated_value)

        return bags

    @classmethod
    def run(cls):
        GBI = GunBotConfigInterface()
        GBI.update_config_from_toml()
        GBI.write_to_gunbot_config()

        while True:
            cls.filter_hot()
            hot = SuperHot.fetch_hot()

            bags = cls.filter_cold()

            cold = [c for c in bags if c not in hot]

            GBI = GunBotConfigInterface()
            GBI.update_config_from_toml()
            GBI.update_pairs(hot, cold, 'binance')  # TODO: Get exchange from a configuration
            GBI.write_to_gunbot_config()

            cls.logger.info(f'Bags: {bags}')
            cls.logger.info(f'Current hot coins in db:{hot}')

            sleep(30)
