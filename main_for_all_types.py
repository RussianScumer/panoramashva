from key_framesver13 import stitch_processed
from stitcher_unprocessed import stitch_unprocessed
import configparser

if __name__ == '__main__':
    settings = configparser.ConfigParser()
    settings.read('settings.ini')
    if settings['WHAT_TYPE_OF_STITCH'] == 'PROCESSED':
        stitch_processed()
    elif settings['WHAT_TYPE_OF_STITCH'] == 'UNPROCESSED':
        stitch_unprocessed()
