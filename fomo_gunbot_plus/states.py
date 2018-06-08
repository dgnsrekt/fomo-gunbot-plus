from abc import ABC, abstractmethod
from time import sleep
from random import choice


class State(ABC):
    """
    Class to define a state object.
    """

    def __init__(self, coin):
        print(f'{coin} state:', str(self))

    @abstractmethod
    def on_event(self, event):
        """
        Handle events that are delegated to this State.
        """
        pass

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


FROZEN = []
COLD = []
HOT = []


class FrozenState(State):
    def __init__(self, coin):
        super().__init__(coin)
        self.coin = coin
        FROZEN.append(self.coin)

    def on_event(self, state):
        if state.lower() == 'cold':
            return self.transition_frozen_to_cold()
        elif state.lower() == 'hot':
            return self.transition_frozen_to_hot()
        else:
            return FrozenState(self.coin)

    def transition_frozen_to_hot(self):
        print(f'{self.coin} transtitioning frozen to hot.')
        FROZEN.remove(self.coin)
        return HotState(self.coin)

    def transition_frozen_to_cold(self):
        print(f'{self.coin} transtitioning frozen to cold.')
        FROZEN.remove(self.coin)
        return ColdState(self.coin)


class ColdState(State):
    def __init__(self, coin):
        super().__init__(coin)
        self.coin = coin
        COLD.append(self.coin)

    def on_event(self, state):
        if state.lower() == 'hot':
            return self.transition_cold_to_hot()
        if state.lower() == 'frozen':
            return self.transition_cold_to_frozen()
        else:
            return ColdState(self.coin)

    def transition_cold_to_hot(self):
        print(f'{self.coin} transtitioning cold to hot.')
        COLD.remove(self.coin)
        return HotState(self.coin)

    def transition_cold_to_frozen(self):
        print(f'{self.coin} transtitioning cold to frozen.')
        COLD.remove(self.coin)
        return FrozenState(self.coin)


class HotState(State):
    def __init__(self, coin):
        super().__init__(coin)
        self.coin = coin
        HOT.append(coin)

    def on_event(self, state):
        if state.lower() == 'cold':
            return self.transition_hot_to_cold()
        elif state.lower() == 'frozen':
            return self.transition_hot_to_frozen()
        else:
            return HotState(self.coin)

    def transition_hot_to_cold(self):
        print(f'{self.coin} transtitioning hot to cold.')
        HOT.remove(self.coin)
        return ColdState(self.coin)

    def transition_hot_to_frozen(self):
        print(f'{self.coin} transtitioning hot to frozen.')
        HOT.remove(self.coin)
        return FrozenState(self.coin)


# FROZEN_FILE = ['BCH', 'BCC']
# COLD_FILE = ['BTC', 'ETC', 'ETH']
# HOT_FILE = ['BKCAT', 'NANO']
#
# coin_states = dict()
#
# for f in FROZEN_FILE:
#     coin_states[f] = FrozenState(f)
#
# for c in COLD_FILE:
#     coin_states[c] = ColdState(c)
#
# for h in HOT_FILE:
#     coin_states[h] = HotState(h)
#
#
# while True:
#     coin = choice(list(coin_states.keys()))
#     state = choice(['hot', 'cold', 'frozen'])
#     print()
#     print('RANDOM', coin, 'Old-State:', coin_states[coin], 'New-State:', state)
#     print('=' * 25)
#     coin_states[coin] = coin_states[coin].on_event(state)
#     sleep(1)
