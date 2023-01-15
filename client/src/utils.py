import argparse
from fileinput import filename
import time
from settings import ALLOWED_MIME_FILE_TYPES

def parse_cmdline_args():
    cmd_parser = argparse.ArgumentParser()

    cmd_parser.add_argument(
        '--server',
        action='store',
        type=str,
        help="remote encrypt/decypt server name or IP.")
    cmd_parser.add_argument(
        '--port',
        action='store',
        type=str,
        help="port number that server is listening to.")

    # mutually exclusive parameters
    group = cmd_parser.add_mutually_exclusive_group()
    group.add_argument(
        '--encrypt',
        action='store',
        type=str,
        help="file that needs to be encrypted.")
    group.add_argument('--decrypt', action='store', type=str,
                       help="file that needs to decrypted. ")
    group.add_argument(
        '--password-hash',
        action='store',
        type=str,
        help="string that needs to be hashed.")

    args = cmd_parser.parse_args()
    return args



def check_filetype(filename):
    ''' detect if file is of specified type'''
    for ft in ALLOWED_MIME_FILE_TYPES:
        if filename.from_file(filename) == ft:
            return True
        else: 
            continue
    return False

