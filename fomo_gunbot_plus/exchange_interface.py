# THIRD PARTY IMPORTS
from ccxt.base.errors import RequestTimeout
import ccxt
import pandas as pd
import structlog


class ExchangeInterface:

    def __init__(self, exchange):
        self.logger = structlog.get_logger()

        self.exchange = ExchangeInterface.connect(exchange)
        self.id = self.exchange.id
        self.logger.debug('Succesfully initialized.', exchange=self.id)

    @classmethod
    def connect(cls,  exchange):
        return getattr(ccxt, exchange)({'enableRateLimit': True})

    def fetch_tickers(self):
        self.logger.debug('Fetching tickers', exchange=self.id)
        tickers = self.exchange.fetchTickers()
        tickers = list(tickers.keys())

        filtered = []
        for t in tickers:
            if '/BTC' in t:
                filtered.append(f"BTC-{t.split('/')[0]}")

        return filtered


class BinanceDataFrameCreator:

    @classmethod
    def prepare_dataframes(cls):
        columns = ['quoteVolume', 'priceChangePercent']
        index = 'symbol'

        exchange = ExchangeInterface('binance')

        unsorted_ticker_data = exchange.pull_tickers()
        sorted_ticker_data = exchange.sort_tickers(unsorted_ticker_data)

        dataframe = pd.DataFrame(sorted_ticker_data)

        columns.append(index)
        columns.append('basecurrency')

        dataframe = dataframe[columns].set_index(index)

        columns.remove(index)
        columns.remove('basecurrency')

        base_pairs = [base for base in dataframe['basecurrency'].unique() if isinstance(base, str)]

        output_data = dict()

        for pair in base_pairs:
            output_data[pair] = dataframe[dataframe['basecurrency'] == pair]
            output_data[pair] = output_data[pair][columns].apply(pd.to_numeric, errors='coerce')
            output_data[pair].columns = ['volume', 'percent_change']

        output_data.pop('USDT')  # dump USDT DATA Filter doesnt like it.

        return output_data
