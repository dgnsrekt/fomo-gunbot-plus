import time

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from .gunbot_interface import GunBotConfigInterface
from .constants import CONFIGURATION_PATH


class ConfigurationHandler(PatternMatchingEventHandler):
    patterns = ['*.toml']

    def process(self, event):
        print(event.src_path, event.event_type)  # TODO: Change to structlog
        GBI = GunBotConfigInterface()
        GBI.update_config_from_toml()
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
