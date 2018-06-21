from .gunbot_interface import GunBotConfigInterface, GunBotStateInterface

from fomo_superfilter.interface import BinanceDataFrameCreator
from fomo_superfilter.superfilter import SuperFilter

from .models.superhot import SuperHot, create_superhot_table
from .models.balance import Balance, create_balance_table
from time import sleep


def display_equity_curve_url():  # IDEA: Move to chart module
    print('Equity Curve Running on...')
    print('* Running on http://127.0.0.1:8050/ (Press CTRL+C to quit)')


def filter_hot():
    print('Searching for hot coins...')
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
        SuperHot.add_coin(hot)
        print(f'Superfilter found {hot}.')


def filter_cold():
    print('Fetching bags...')
    gbot_pipe = GunBotStateInterface()

    bags = gbot_pipe.fetch_bags
    all_pairs = gbot_pipe.all_pairs

    if not Balance.table_exists():
        create_balance_table()

    Balance.add(gbot_pipe.estimated_value)

    return bags, all_pairs


def run():

    GBI = GunBotConfigInterface()
    GBI.update_config_from_toml()
    GBI.write_to_gunbot_config()

    while True:
        filter_hot()
        bags, all_pairs = filter_cold()
        superhot = SuperHot.fetch_hot()

        print(f'bags: {bags}')
        print(f'pairs: {all_pairs}')
        print(f'Current hot coins in db:{superhot}')

        # others_current = [other for other in binance_names if other not in hot_current]
        # print(len(binance_names))
        # print(len(others_current))

        sleep(30)
