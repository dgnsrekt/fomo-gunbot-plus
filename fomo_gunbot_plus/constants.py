# SYSTEM IMPORTS
from pathlib import Path

BASEPATH = Path(__file__).parent

CLEAN_JSON_CONFIG_PATH = BASEPATH.parent / 'clean.json'

CONFIGURATION_PATH = BASEPATH.parent / 'configuration'

CONFIGFILE_PATH = BASEPATH.parent / 'config.toml'

STATE_PATH = BASEPATH.parent / 'states.toml'

DELISTED_PATH = BASEPATH.parent / 'delisted.toml'

GUNBOT_PATH = BASEPATH.parent / 'gunbot'

CONFIG_JS_PATH = GUNBOT_PATH / 'config.js'

GUNBOT_DOWNLOAD_PATH = BASEPATH.parent / 'lin.zip'

TEMP_GUNBOT_EXTRACTPATH = BASEPATH.parent / 'gunbot_temp'
