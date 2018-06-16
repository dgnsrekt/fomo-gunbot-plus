from fomo_gunbot_plus.gunbot_interface import GunBotConfigInterface


def test_import():
    pass


def test_gunbot_init():
    GBI = GunBotConfigInterface()
    GBI.config.pop('pairs')
    assert GBI.toml_config.keys() == GBI.config.keys()
    assert GBI.toml_config == GBI.config


def test_gunbot_toml_config_diff():
    GBI = GunBotConfigInterface()
    assert GBI.toml_config.keys() != GBI.config.keys()
    assert GBI.toml_config != GBI.config

# Will need to use some temp files maybe
# def test_upddate_config_from_toml():
#     GBI = GunBotConfigInterface()
#     C1 = GBI.config
#     GBI.update_config_from_toml()
#     C2 = GBI.config
#     assert C1 == C2
