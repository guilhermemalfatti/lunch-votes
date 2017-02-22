import os
from configparser import ConfigParser
from app.util.singleton import Singleton

class Config(metaclass=Singleton):
    """ Config singleton

    This class provides a single instance to the configuration values for the project.
    """

    def __init__(self):
        config = ConfigParser()
        config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini'))

        self.config = config

    def get_config(self):
        return self.config

    def get_value(self, section, key):
        try:
            return self.config[section][key]
        except Exception:
            return None
