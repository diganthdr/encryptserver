from datetime import datetime
import logging

from encdec.algos.aes import aes
from utils import write_to_file, parse_cmdline_args


def request_router(filename, operation, algo='AES'):
    """ in: filename: file name which needs to be encrypted/decrypted
            operation: encrypt/decrypt
            algo: algorithm to be used for enc/dec
        out: filename of the generated file """
    # Below map contains algo vs function to be called table.
    # This helps to maintain supported algo list and implement new feature
    # easily.
    router_map = {
        'AES': aes
    }

    logging.debug(f"Request rcvd, file: {filename}, operation: {operation} with algo: {algo}")
    if algo not in router_map.keys():
        raise NotImplementedError(
            f"Algorithm {algo} not implemented or supported")

    # dev note: This 'strategy' avoids never ending if-else conditions
    byte_stream = router_map[algo](filename, operation)
    timestamped_filename = write_to_file(byte_stream, filename, operation)
    logging.debug(f"output file: {timestamped_filename}")

    return timestamped_filename 


# test purpose only
if __name__ == '__main__':
    args = parse_cmdline_args()
    out_json = request_router(args.filename, args.operation, args.algo)
    print(out_json)
