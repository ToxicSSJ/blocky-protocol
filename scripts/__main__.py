from log.logger import init_logger

import os
import glob
import time
import configparser
import colorama, coloredlogs, logging

colorama.init()
logger = init_logger("", True)

def _main():
    logger.info('Starting the basic setup procedure...')

    '''
    Read the ini config
    for the custom attributes
    '''
    config = configparser.ConfigParser()
    config.read(glob.glob('../config/config.ini'))

    '''
    Freeze main thread
    '''
    try:
        while True:
            time.sleep(1000)
    except KeyboardInterrupt:
        logger.info("Proccess stopped!")

if __name__ == '__main__':
    _main()