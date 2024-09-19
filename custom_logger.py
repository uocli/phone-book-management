import logging
import os

log_filename = './system.log'
log_directory = os.path.dirname(log_filename)
os.makedirs(log_directory, exist_ok=True)

logger = logging.getLogger(__name__)
logger.propagate = False

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

file_handler = logging.FileHandler(log_filename, mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
