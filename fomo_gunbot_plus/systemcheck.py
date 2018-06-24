# SYSTEM IMPORTS
import json
import shutil
from pathlib import Path

# THIRD PARTY IMPORTS
import luigi
import structlog
import toml
import wget
from zipfile import ZipFile

# LOCAL IMPORTS
from .configuration import Configuration
from .constants import (BASEPATH,
                        CONFIGURATION_PATH,
                        CONFIGFILE_PATH,
                        CLEAN_JSON_CONFIG_PATH,
                        TEMP_GUNBOT_EXTRACTPATH,
                        GUNBOT_DOWNLOAD_PATH,
                        STATE_PATH,
                        DELISTED_PATH,
                        GUNBOT_PATH,
                        CONFIG_JS_PATH)

from .gunbot_interface import GunBotConfigInterface


class DownloadGunBotTask(luigi.Task):

    def output(self):
        return luigi.LocalTarget(str(GUNBOT_DOWNLOAD_PATH))

    def run(self):
        url = 'https://github.com/GuntharDeNiro/BTCT/releases/download/951_b532/lin.zip'
        wget.download(url, self.output().path)


class GunbotFolderCheckTask(luigi.Task):

    def requires(self):
        return DownloadGunBotTask()

    def output(self):
        paths = [GUNBOT_PATH,
                 GUNBOT_PATH / 'config.js',
                 GUNBOT_PATH / 'gunthy-gui',
                 GUNBOT_PATH / 'gunthy-linx64',
                 GUNBOT_PATH / 'node_sqlite3.node',

                 GUNBOT_PATH / 'node_modules/',
                 GUNBOT_PATH / 'node_modules/sqlite3/',
                 GUNBOT_PATH / 'node_modules/sqlite3/lib/',
                 GUNBOT_PATH / 'node_modules/sqlite3/lib/binding/',
                 GUNBOT_PATH / 'node_modules/sqlite3/lib/binding/node-v57-darwin-x64/',
                 GUNBOT_PATH / 'node_modules/sqlite3/lib/binding/node-v57-darwin-x64/node_sqlite3.node',
                 GUNBOT_PATH / 'node_modules/sqlite3/lib/binding/node-v57-linux-x64/',
                 GUNBOT_PATH / 'node_modules/sqlite3/lib/binding/node-v57-linux-x64/node_sqlite3.node',

                 GUNBOT_PATH / 'node_modules/websocket/',
                 GUNBOT_PATH / 'node_modules/websocket/build/',
                 GUNBOT_PATH / 'node_modules/websocket/build/Release/',
                 GUNBOT_PATH / 'node_modules/websocket/build/Release/bufferutil.node',
                 GUNBOT_PATH / 'node_modules/websocket/build/Release/validation.node',

                 GUNBOT_PATH / 'tulind/',
                 GUNBOT_PATH / 'tulind/lib/',
                 GUNBOT_PATH / 'tulind/lib/binding/',
                 GUNBOT_PATH / 'tulind/lib/binding/Release/',
                 GUNBOT_PATH / 'tulind/lib/binding/Release/node-v57-darwin-x64/',
                 GUNBOT_PATH / 'tulind/lib/binding/Release/node-v57-darwin-x64/tulind.node',
                 GUNBOT_PATH / 'tulind/lib/binding/Release/node-v57-linux-arm/',
                 GUNBOT_PATH / 'tulind/lib/binding/Release/node-v57-linux-arm/tulind.node',
                 GUNBOT_PATH / 'tulind/lib/binding/Release/node-v57-linux-x64/',
                 GUNBOT_PATH / 'tulind/lib/binding/Release/node-v57-linux-x64/tulind.node',
                 ]

        luigi_paths = [luigi.LocalTarget(str(p)) for p in paths]
        return luigi_paths

    def run(self):
        if GUNBOT_PATH.exists():
            shutil.rmtree(str(GUNBOT_PATH))

        zip = ZipFile(self.input().path)
        zip.extractall(str(TEMP_GUNBOT_EXTRACTPATH))
        zip.close()

        assert (TEMP_GUNBOT_EXTRACTPATH/'lin').exists()

        shutil.move(str(TEMP_GUNBOT_EXTRACTPATH/'lin'), self.output()[0].path)
        assert GUNBOT_PATH.exists()

        shutil.rmtree(str(TEMP_GUNBOT_EXTRACTPATH))
        assert not TEMP_GUNBOT_EXTRACTPATH.exists()


class CleanJsonTask(luigi.Task):
    def requires(self):
        return GunbotFolderCheckTask()

    def output(self):
        return luigi.LocalTarget(str(CLEAN_JSON_CONFIG_PATH))

    def run(self):
        path_ = Path(self.input()[0].path) / 'config.js'
        with open(path_, 'r') as f:
            data = json.loads(f.read())

        with open(self.output().path, 'w') as f:
            f.write(json.dumps(data, indent=4))


class TomlConfigCheckTask(luigi.Task):

    def requires(self):
        return CleanJsonTask()

    def output(self):

        paths = [
            CONFIGURATION_PATH,
            CONFIGURATION_PATH / 'bot.toml',
            CONFIGURATION_PATH / 'exchanges.toml',
            CONFIGURATION_PATH / 'imap_listener.toml',
            CONFIGURATION_PATH / 'strategies.toml',
            CONFIGURATION_PATH / 'version.toml',
            CONFIGURATION_PATH / 'ws.toml']

        luigi_paths = [luigi.LocalTarget(str(p)) for p in paths]
        return luigi_paths

    def run(self):
        dir_ = Path(self.output()[0].path)
        dir_.mkdir()
        assert dir_.exists()

        GBI = GunBotConfigInterface()


class MainConfigTomlTask(luigi.Task):

    def output(self):
        return luigi.LocalTarget(str(CONFIGFILE_PATH))

    def run(self):
        config = Configuration()


class SystemCheckTask(luigi.WrapperTask):

    def requires(self):
        return [GunbotFolderCheckTask(), TomlConfigCheckTask(), MainConfigTomlTask()]


class SystemCheck:

    logger = structlog.get_logger()

    @classmethod
    def run(cls):
        cls.logger.info('Running Systems Checks...')
        return luigi.build([SystemCheckTask()], local_scheduler=True)
