from pathlib import Path

BASEPATH = Path(__file__).parent

CONFIGURATION_PATH = BASEPATH.parent / 'configuration'
assert CONFIGURATION_PATH.exists(), f'{CONFIGURATION_PATH} file missing.'

CLEAN_JSON_CONFIG_PATH = BASEPATH.parent / 'clean.json'
assert CLEAN_JSON_CONFIG_PATH.exists(), f'{CLEAN_JSON_CONFIG_PATH} file missing.'

STATE_PATH = BASEPATH.parent / 'states.toml'  # TODO: Change to toml
assert STATE_PATH.exists(), f'{STATE_PATH} file missing.'

GUNBOT_PATH = BASEPATH.parent / 'gunbot'
assert GUNBOT_PATH.exists(), f'{STATE_PATH} file missing.'  # TODO addmessage may need download gb

CONFIG_JS_PATH = GUNBOT_PATH / 'config.js'
assert CONFIG_JS_PATH.exists(), f'{STATE_PATH} file missing.'
