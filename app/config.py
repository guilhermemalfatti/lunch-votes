import os
from configparser import ConfigParser
from app.util.singleton import Singleton
from app import logger


class Config(metaclass=Singleton):
    """ Config singleton

    This class provides a single instance to the configuration values for the project.
    """

    def __init__(self):
        """
        Starts a Config instance
        """
        logger.info('start read general configs')
        config = ConfigParser()
        config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini'))

        self.config = config

    def get_config(self):
        """
        return the configs
        """
        logger.info('start get_config.')
        return self.config

    def get_value(self, section, key):
        """
        return the valu of config by section and key
        """
        logger.info('start get value on config')
        try:
            logger.debug('config value: ' + str(self.config[section][key]))
            return self.config[section][key]
        except Exception:
            return None
