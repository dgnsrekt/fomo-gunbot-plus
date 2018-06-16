from fomo_gunbot_plus import states
from fomo_gunbot_plus.states import FrozenState, ColdState, HotState


def test_import():
    pass

#----FROZEN TEST


def test_frozen_to_frozen():
    btc = FrozenState('BTC')
    assert btc.coin == 'BTC'
    assert isinstance(btc, FrozenState)

    btc = btc.on_event('frozen')
    assert isinstance(btc, FrozenState)


def test_frozen_to_cold():
    btc = FrozenState('BTC')
    assert btc.coin == 'BTC'
    assert isinstance(btc, FrozenState)

    btc = btc.on_event('cold')
    assert isinstance(btc, ColdState)


def test_frozen_to_hot():
    btc = FrozenState('BTC')
    assert btc.coin == 'BTC'
    assert isinstance(btc, FrozenState)

    btc = btc.on_event('hot')
    assert isinstance(btc, HotState)

#----HOT TEST


def test_hot_to_hot():
    btc = HotState('BTC')
    assert btc.coin == 'BTC'
    assert isinstance(btc, HotState)

    btc = btc.on_event('hot')
    assert isinstance(btc, HotState)


def test_hot_to_cold():
    btc = HotState('BTC')
    assert btc.coin == 'BTC'
    assert isinstance(btc, HotState)

    btc = btc.on_event('cold')
    assert isinstance(btc, ColdState)


def test_hot_to_frozen():
    btc = HotState('BTC')
    assert btc.coin == 'BTC'
    assert isinstance(btc, HotState)

    btc = btc.on_event('frozen')
    assert isinstance(btc, FrozenState)

#----COLD TEST


def test_cold_to_cold():
    btc = ColdState('BTC')
    assert btc.coin == 'BTC'
    assert isinstance(btc, ColdState)

    btc = btc.on_event('cold')
    assert isinstance(btc, ColdState)


def test_cold_to_frozen():
    btc = ColdState('BTC')
    assert btc.coin == 'BTC'
    assert isinstance(btc, ColdState)

    btc = btc.on_event('frozen')
    assert isinstance(btc, FrozenState)


def test_cold_to_hot():
    btc = ColdState('BTC')
    assert btc.coin == 'BTC'
    assert isinstance(btc, ColdState)

    btc = btc.on_event('hot')
    assert isinstance(btc, HotState)
