'''This module contains functions for logging errors'''
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

LOG_FORMAT = '%(asctime)s - %(filename)s - %(message)s'
logging.basicConfig(filename='error.log', format=LOG_FORMAT,
                    datefmt='%Y-%m-%d %H:%M:%S')


def log_error(error_msg):
    '''Logs an error message'''
    logger.error(error_msg, exc_info=True)
