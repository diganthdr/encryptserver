# some default values
import logging

logging.basicConfig(filename='crypto-client-cli.log', encoding='utf-8', level=logging.DEBUG) #TODO: Add log rotation
logger = logging.getLogger("server_log")

HTTP_PREFIX = "http://"
SERVER_HOSTNAME = "localhost"
PORT = 5000

UPLOAD_ENDPOINT = "fileupload"
DOWNLOAD_ENDPOINT = "filedownload"
TASK_STATUS_ENDPOINT = "taskstatus"
HASHIFY_ENDPOINT = "hash"

TASK_STATUS_API_TIMEOUT = 10  # seconds
DELAY_SECONDS = 1  # check every DELAY_SECONDS in a loop

ALLOWED_MIME_FILE_TYPES = ['text/plain']