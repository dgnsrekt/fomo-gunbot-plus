# SYSTEM IMPORTS
from abc import ABC, abstractmethod
from random import choice
from time import sleep

# LOCAL IMPORTS
from .configuration import Configuration


class State(ABC):
    """
    Class to define a state object.
    """

    def __repr__(self):
        """
        Leverages the __str__ method to describe the State.
        """
        return self.__str__()

    def __str__(self):
        """
        Returns the name of the State.
        """
        return self.__class__.__name__


class ColdState(State):
    def __init__(self, coins):
        self.coins = coins
        self.enabled = True
        self.pair_configuration = dict()
        self.pair_configuration['strategy'] = 'emotionless'
        self.pair_configuration['override'] = {'BUY_ENABLED': False, 'GAIN': 0.5}

    def prepare_config(self):
        config = dict()
        for coin in self.coins:
            name = f'BTC-{coin}'.upper()
            config[name] = self.pair_configuration
        return config


class DumpState(State):
    def __init__(self, coins):
        self.settings = Configuration()
        self.dump_bags = self.settings.general['DUMP_BAGS_OVER_24H_OLD']

        self.coins = coins
        self.enabled = True
        self.pair_configuration = dict()
        self.pair_configuration['strategy'] = 'emotionless'

        if self.dump_bags:
            self.pair_configuration['override'] = {'PANIC_SELL': True}
        else:
            self.pair_configuration['override'] = {'BUY_ENABLED': False, 'GAIN': 0.25}

    def prepare_config(self):
        config = dict()
        for coin in self.coins:
            name = f'BTC-{coin}'.upper()
            config[name] = self.pair_configuration
        return config


class HotState(State):
    def __init__(self, coins):
        self.coins = coins
        self.enabled = True
        self.pair_configuration = dict()
        self.pair_configuration['strategy'] = 'emotionless'
        self.pair_configuration['override'] = {}

    def prepare_config(self):
        config = dict()
        for coin in self.coins:
            name = f'BTC-{coin}'.upper()
            config[name] = self.pair_configuration
        return config
