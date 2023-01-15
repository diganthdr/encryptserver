import os
from asyncio.log import logger
from datetime import datetime

from settings import OUTPUT_FILE_SUFFIX, logger


def write_to_file(byte_stream, filename, operation):
    """ in: bytes
    out: filename with timestamp appended to make sure filenames do not clash
    """
    now = datetime.now()  # current date and time
    date_time_timestamp = now.strftime("%m_%d_%Y_%H_%M_%S")
    # scalability note: better would be to use uuid
    filename = '_'.join([filename, date_time_timestamp,
                        OUTPUT_FILE_SUFFIX[operation]])

    try:
        with open(filename, 'wb') as fd:
            fd.write(byte_stream)
    except Exception as e:
        logger.error(f"Something went wrong while writing to file: {e}")


    return os.path.abspath(filename)

def parse_cmdline_args():
    import argparse
    cmd_parser = argparse.ArgumentParser()
    cmd_parser.add_argument('--filename',
                            action='store',
                            type=str,
                            required=True)
    cmd_parser.add_argument('--operation', action='store', type=str)
    cmd_parser.add_argument('--algo', action='store', type=str)
    args = cmd_parser.parse_args()
    return args