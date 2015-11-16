from __future__ import print_function

import os
import logging
from datetime import datetime
import time


PREFIXES = ['IMG', 'PIC', 'PANO', 'VID']
EXTENSIONS = ['.JPG', '.JPEG', '.MP4']
DEFAULT_FMT = "%Y%m%d_%H%M%S"

# My camera(s) have output like "PREFIX_20150131_121500_SUFFIX.JPG", where both prefix and suffixes are
# optional, with JPG and MP4 extensions. I've added the ".JPEG" extension for compatibility with some
# weird picture processing apps that I have, which change JPG to JPEG. Also, PANO is added to be compatible
# with Google Photos, which automatically adds this prefix when creating panoramas.

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)  # If anything goes wrong, set logging level to logging.DEBUG to see what's up


def update_timestamps(root='.', fmt=None):
    """
    Updates timestamps of all files (with regards to PREFIXES and EXTENSIONS) according to filenames
    :param root: where to start processing from
    :param fmt: format to feed datetime.datetime.strptime
    :return: None
    """
    logging.debug('Running update timestamps...')
    for folder, _, files in os.walk(root):
        for f in files:
            pth = os.path.abspath(os.path.join(folder, f))
            logging.debug('Working on "%s"' % pth)
            dt, ok = parse_filename(f, fmt)

            if ok:
                timestamp = to_epoch(dt)
                try:
                    os.utime(pth, (timestamp, timestamp))
                    logger.debug('File "%s" OK.' % pth)
                except Exception as e:
                    logger.error('Could not change timestamp for file "%s": "%s"' % (pth, e))
    logger.debug('Finished.')


def parse_filename(file_name, fmt=None):
    """
    Parses filename to return a datetime or None (second param being True or False
    depending on if the parsing was successful or not)
    :param fmt: format to feed to datetime.datetime.strptime
    :param file_name: file name in format [prefix_]YYYYMMDD_HHMMSS[_suffix].EXT
    :return: (dt, True) or (None, False)
    """

    fmt = fmt or DEFAULT_FMT
    name, ext = os.path.splitext(file_name)

    if ext.upper() not in EXTENSIONS:
        logger.debug('Extension not in allowed list of extensions: "%s"' % ext)
        return None, False

    chunks = name.split('_')
    if len(chunks) < 2:
        logger.debug('Wrong number of chunks: minimum is 2.')
        return None, False

    elif len(chunks) == 2:
        timestr = '_'.join([chunks[0][:8], chunks[1][:6]])
        return parse_timestr(timestr, fmt)

    elif len(chunks) >= 3:
        logger.debug('Three or more chunks detected: "%s"' % chunks)

        if chunks[0].isdigit():
            # assumes YYYYMMDD_HHMMSS_SUFFIX(ES)
            timestr = '_'.join([chunks[0][:8], chunks[1][:6]])
            return parse_timestr(timestr, fmt)

        else:
            # assumes PREFIX_YYYYMMDD_HHMMSS_SUFFIX(ES)
            _prefix = chunks[0]
            if _prefix.upper() not in PREFIXES:
                logger.debug('Prefix "%s" not in the list of allowed prefixes.' % _prefix)
                return None, False

            timestr = '_'.join([chunks[1][:8], chunks[2][:6]])
            return parse_timestr(timestr, fmt)


def parse_timestr(timestr, fmt):
    """
    Parse time string in format fmt, return (datetime.datetime, bool)
    :param timestr: A string to parse
    :param fmt: format to feed to datetime.datetime.strptime
    :return: (datetime.datetime or None, True or False), eg: (None, False) if failed
    """
    try:
        dt = datetime.strptime(timestr, fmt)
        success = True
    except ValueError:
        logger.debug('Wrong format: "%s"' % timestr)
        dt = None
        success = False
    except Exception as e:
        logger.exception('Unknown error occurred: "%s"' % e)
        dt = None
        success = False
    return dt, success


def to_epoch(dt):
    """ Convert datetime to epoch int
    :param dt: instance of datetime.datetime
    :return: int, unix timestamp (without ms)
    """
    return int(time.mktime(dt.timetuple()))

