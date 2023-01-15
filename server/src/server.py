# flask app.

import os
import sys
import traceback
import urllib.request
import argparse
from pathlib import Path
from flask import Flask, request, redirect, jsonify, send_file
from werkzeug.utils import secure_filename
from celery.result import AsyncResult

from driver import request_router
from generatehash import generate_hash
from celeryapp import router_task
from settings import FILE_UPLOAD_DIR, logger

global_tasks = {}
ALLOWED_EXTENSIONS = set(['txt'])
ALLOWED_OPERATIONS = ["encrypt", "decrypt"]
UPLOAD_DIR = "uploaded_files"

app = Flask(__name__)


def allowed_file(filename, operation):
    if operation == 'encrypt':
        return '.' in filename and filename.rsplit(
            '.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return True  # for decrypt, allow any file. TODO: Think, how can we know its encrypted


@app.route("/filedownload", methods=['GET', 'POST'])
def download_file():
    """ interface to download file which is processed. Either encrypted or decrypted """

    taskid = None
    if 'task_id' not in request.form:
        resp = jsonify({'message': 'No jobid specified in the request'})
        resp.status_code = 400
        return resp

    else:
        taskid = request.form['task_id']
        if taskid not in global_tasks.keys():
            resp = jsonify({
                'message': 'task id not found',
                'task_id': taskid,
            })
            resp.status_code = 400
            logger.debug(f"Task ID: {taskid} not found")
            return resp

    try:
        logger.debug(f"sending file: {global_tasks[taskid]}")
        return send_file(global_tasks[taskid], as_attachment=True)
        #return send_file(global_tasks[taskid], mimetype='application/x-binary', as_attachment=True)
    except Exception as e:
        logger.debug(f"Exception: {e}, {traceback.print_exception(*sys.exc_info())}")
        resp = jsonify({'message': 'internal server error while sending file'})
        resp.status_code = 500
        return resp


@app.route('/fileupload', methods=['POST'])
def upload_file():
    """ Iterface to upload file, file is stored locally for further processing """
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp

    uploaded_file = request.files['file']

    if 'operation' not in request.form:
        resp = jsonify({'message': 'No operation specified in the request'})
        resp.status_code = 400
        return resp

    if request.form['operation'] not in ALLOWED_OPERATIONS:
        resp = jsonify(
            {'message': f'Operation not supported. Supported operations are {ALLOWED_OPERATIONS}'})
        resp.status_code = 400
        return resp

    operation = request.form['operation']

    if uploaded_file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp

    if uploaded_file and allowed_file(uploaded_file.filename, operation):
        # download file and save
        _filename = secure_filename(uploaded_file.filename) # security: make sure input is sanitised
        Path(FILE_UPLOAD_DIR).mkdir(exist_ok=True)
        uploaded_file_path = os.path.join(FILE_UPLOAD_DIR, _filename)
        uploaded_file.save(uploaded_file_path)
        logger.debug(f"File saved at {uploaded_file_path}")

        # resp = request_router(uploaded_file_path, operation) #Non-async
        task_rc = router_task.delay(uploaded_file_path, operation)  # async

        msg = f"id: {task_rc.id}, status: {task_rc.status}"
        logger.debug(f"Task created,{msg}")

        # TODO: we can move to DB to make it robust, but for now..
        global_tasks[task_rc.id] = None

        driver_response = {"task_id": task_rc.id}

        if "error" in driver_response:
            logger.error(f"{driver_response}")
            driver_response.update({"message": "failure"})
            resp = jsonify(driver_response)
            resp.status_code = 400
        else:
            driver_response.update(
                {"message": "successfully sent to process queue"})
            resp = jsonify(driver_response)
            resp.status_code = 201

        return resp

    else:
        resp = jsonify({
            'message':
            f'Allowed file types are {list(ALLOWED_EXTENSIONS)}'
        })
        resp.status_code = 400
        return resp


@app.route('/taskstatus', methods=['GET', 'POST'])
def task_status():
    if 'task_id' not in request.form:
        resp = jsonify({'message': 'task id not specified'})
        resp.status_code = 400
        return resp

    taskid = request.form['task_id']
    if taskid not in global_tasks.keys():
        resp = jsonify({
            'message': 'task id not found',
            'task_id': taskid,
        })
        resp.status_code = 400
        logger.error(f"Task id {taskid} not found in {global_tasks}")
        return resp

    state = router_task.AsyncResult(taskid).state
    resp = {'task_id': taskid, 'task_status': state}

    # this does not assure acual process is success, just worker is finished.
    if state == "SUCCESS":
        resp['result'] = router_task.AsyncResult(taskid).get()
        global_tasks[taskid] = resp['result']

    resp = jsonify(resp)
    resp.status = 200
    return resp


@app.route('/hash', methods=['GET'])
def hashify():
    hashstr = None
    if 'password' not in request.form:
        resp = jsonify({'message': 'password not specified'})
        resp.status_code = 400
        return resp

    password = request.form['password']
    if len(password) > 20:
        resp = jsonify({'message': 'Password must be less than 20 chars.'})
        resp.status_code = 400
        return resp

    hashstr = generate_hash(password)
    if hashstr:
        resp = jsonify({'hash': f'{hashstr}'})  # bytes
        return resp

    logger.error("Unable to generate hash.")
    resp = jsonify({
        'error': "problem in generating hash",
    })
    resp.status_code = 400

    return resp


@app.route('/test', methods=['GET'])
def isapprunning():  # Debug API
    # check if the post request has the file part
    resp = jsonify({'message': 'Backend is up and running!'})
    return resp


def parse_cmdline_args():
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--host', action='store', type=str)
    my_parser.add_argument('--port', action='store', type=str)
    args = my_parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_cmdline_args()
    if args:
        app.run(host=args.host, port=args.port)
    else:  # default
        app.run(host="0.0.0.0", port=5000)
