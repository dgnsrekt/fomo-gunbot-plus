# SYSTEM IMPORTS
import time

# THIRD PARTY IMPORTS
import structlog
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

# LOCAL IMPORTS
from .gunbot_interface import GunBotConfigInterface
from .constants import CONFIGURATION_PATH


class ConfigurationHandler(PatternMatchingEventHandler):
    logger = structlog.get_logger()
    patterns = ['*.toml']

    def process(self, event):
        self.logger.info(f'{event.src_path}|{event.event_type}')
        GBI = GunBotConfigInterface()
        GBI.update_config_from_toml()
        GBI.update_pairs_from_live()
        GBI.write_to_gunbot_config()

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


def watch_configuration_folder():
    observer = Observer()
    observer.schedule(ConfigurationHandler(), path=str(CONFIGURATION_PATH))
    observer.start()

    try:
        while True:
            time.sleep(1)
    except:
        observer.stop()
    observer.join()
