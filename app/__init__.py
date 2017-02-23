import logging.config
import os

logging.config.fileConfig(os.path.abspath(os.path.dirname(__file__)) + "/logging.conf")

# create logger
logger = logging.getLogger(__name__)
