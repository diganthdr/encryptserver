import imp
from pathlib import Path
import os

import logging
logging.basicConfig(filename='crypto-server.log', encoding='utf-8', level=logging.DEBUG) #TODO: Add log rotation
logger = logging.getLogger("clientlog")

SECRET_KEY_AES = 'Wm43JqFf3zrtIaKqbEqzPxoWE92eyRNT' #TODO: Not a good idea to keep here. Can be stored at remote secure server.

ENCRYPTED_FILE_SUFFIX = "encrypted.txt"
DECRYPTED_FILE_SUFFIX = "decrypted.txt"

OUTPUT_FILE_SUFFIX = {
    "encrypt": ENCRYPTED_FILE_SUFFIX,
    "decrypt": DECRYPTED_FILE_SUFFIX
}

# go above ./src
FILE_UPLOAD_DIR = os.path.join(Path.cwd().parent.absolute(), "uploaded_files")
