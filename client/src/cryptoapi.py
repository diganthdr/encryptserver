import os
import requests
import sys
import time

from settings import HTTP_PREFIX, SERVER_HOSTNAME, PORT, UPLOAD_ENDPOINT, \
    DOWNLOAD_ENDPOINT, TASK_STATUS_ENDPOINT, HASHIFY_ENDPOINT, \
    TASK_STATUS_API_TIMEOUT, DELAY_SECONDS, ALLOWED_MIME_FILE_TYPES, logger
from utils import parse_cmdline_args 

MAX_MB = 10
MAX_TEXT_FILE_SIZE = 1000000*MAX_MB
BUG_REPORT_MESSAGE = "Report bug: https://github.com/woven-planet-security-hiring/diganthdr-dast-challenge/blob/main/README.md#bug-reporting"

def cmd_hashify(password, server=SERVER_HOSTNAME, port=PORT):
    payload = {'password': password}
    logger.debug("Hasify called") #Security: Do NOT ever log password.
    url = HTTP_PREFIX + "/".join([server + f":{port}", HASHIFY_ENDPOINT])
    api_response = requests.get(url, data=payload)
    
    if api_response.status_code == 200:
        print(api_response.json())
        return api_response

    err_msg = f"Unexpected status_code: {api_response.status_code}, response: {api_response}"
    logger.error(err_msg)
    print(err_msg)
    print()
    return api_response


def download_processed_file(filename, operation, taskid, server, port):
    """ Downloads file from server based on task id.
    params filename and operation is just for file saving """

    # TODO: for big files, probably download in chunks
    url = HTTP_PREFIX + "/".join([server + f":{port}", DOWNLOAD_ENDPOINT])
    files = {'file': open(filename, 'rb')}
    payload = {'task_id': taskid}

    res = requests.get(url, data=payload)
    if res.status_code==500:
        logger.error(f"Something went wrong at server while downloading file.")
        print(f"ERROR: Something went wrong at server while downloading file.")

    print("Downloading processed file...")
    try:
        with open(filename + "." + operation, 'wb') as fd:
            fd.write(res.content)
            print(f"Saved to: {fd.name}")
    except Exception as e:
        logger.error(f"Something went wrong while writing file {fd.name}. Exception: {e}")


def poll_remote_task(taskid, timeout, delay, server, port):

    while (timeout > 0): #TODO: refactor this!
        payload = {'task_id': taskid}
        url = HTTP_PREFIX + \
            "/".join([server + f":{port}", TASK_STATUS_ENDPOINT])
        task_response = requests.get(url, data=payload)

        if task_response.status_code == 200:
            response_dict = task_response.json()

            if response_dict['task_status'] == "SUCCESS":
                print("Task is successfully completed at server.")
                break

            elif response_dict['task_status'] == "PENDING":
                timeout = timeout - delay
                time.sleep(delay)
            else:
                logger.error(f"Task {response_dict['task_id']} is in unexpected state. {response_dict['task_status']}")
                print(
                    "Task is in unexpected state: ",
                    response_dict['task_status'])
                print(BUG_REPORT_MESSAGE)
                sys.exit()

def cmd_encrypt_decrypt(filename, operation, server, port):  # TODO: refactor this
    """ sends request to remote server with params below.
    in:
            filename: filename to be uploaded
            operation: enc/decrypt/hash
            server: remote server address, by default localhost
            port: remote server's port number. default is 5000
    out: None. request responses are handled. """

    # step 1:
    url = HTTP_PREFIX + "/".join([server + f":{port}", UPLOAD_ENDPOINT])
    logger.debug(f"CMD_ENC_DEC: {filename}, {operation}, {server}, {port} \n URL formed:{url}")
    
    if operation=='encrypt' and MAX_TEXT_FILE_SIZE < os.path.getsize(filename):
        print("File is too big. current MAX_SIZE supported is", MAX_MB, "MB", "File size is:", os.path.getsize(filename))
        sys.exit()

    # print(url)
    files = {'file': open(filename, 'rb')}
    payload = {'file': filename, 'operation': operation}
    res = requests.post(url, data=payload, files=files)
    logger.debug(f"Response: {res.status_code}")

    if res.status_code == 201:
        response_dict = res.json()
        print("Fetching output from remote task...")
    else:
        print("Unable to get expected response.")
        logger.error(f"Unexpected response.{res.status_code}")
        sys.exit()

    # step 2: wait on remote task.
    if 'task_id' in response_dict.keys():
        poll_remote_task(response_dict['task_id'], TASK_STATUS_API_TIMEOUT, DELAY_SECONDS ,server, port)
    else:
        logger.error("File upload failed")
        print("ERROR: File upload failed.")
        print(res.json())
        sys.exit()

    #Step 3: Download
    download_processed_file(filename, operation, response_dict['task_id'], server, port)




def run():
    args = parse_cmdline_args()
    logger.debug(f"Command line args rcvd: {args}")

    server = SERVER_HOSTNAME
    port = PORT

    if args.server:
        server = args.server
        if args.port:
            port = args.port
        else:
            print("Please specify port")
            sys.exit()

    try:
        if args.encrypt:
            cmd_encrypt_decrypt(args.encrypt, 'encrypt', server, port)

        if args.decrypt:
            cmd_encrypt_decrypt(args.decrypt, 'decrypt', server, port)

        if args.password_hash:
            cmd_hashify(args.password_hash, server, port)

    except requests.exceptions.ConnectionError as ce:
        print(f"Unable to connect to server: {server}, port {port}")
        logger.error(f"Unable to connect to server: {server}, port {port}")
        sys.exit()

    except FileNotFoundError as fe:
        print(f"File not found. Is that a typo? or Are you in different dir?")

    except Exception as generic_exception:
        print("Encountered unknown exception. Please check logs. If it looks like bug,")
        print(BUG_REPORT_MESSAGE)
        print(str(generic_exception))
        logger.error(f"Exception: {generic_exception}")
        sys.exit()


if __name__ == '__main__':
    run()

    # TODO: Visualisation feature: steps progress bar, like.. 1/3. connecting
    # to server. 2/3 fetching key, 3/3 uploading file.
