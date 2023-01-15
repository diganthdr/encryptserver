#!/bin/bash    

DASHLINE="---------------------------------"
CWD=`pwd`

EXEC_STATUS(){
    if [ $? -eq 0 ]; then
        echo OK
    else
        echo FAIL
        cd $PWD
        exit
    fi
}

BRING_UP(){

echo $DASHLINE
# start redis. Note this is simplest redis server with no auth, deamon or anything like that.
echo "Starting redis server..."
redis-server > redis-server.log & 
EXEC_STATUS

sleep 3 # wait for redis to start
echo DASHLINE
# start celery workers
echo "Starting celery workers..."
cd server/src && celery -A celeryapp.celery  worker --loglevel=DEBUG --logfile=../../celery.log & 
EXEC_STATUS
cd $CWD

# start flask server. TODO: Integrate wsgi server. This is for dev context.
sleep 3 # wait for celery to get up
echo $DASHLINE
echo "Starting  server..."
cd server/src && python3 server.py > ../../server.log &
cd $CWD
}



BRING_UP

# run some client command to check if sever is up and running.
sleep 5 # wait for server to come up
# TODO: ADD command to environment
echo "Check command password-hash as smoke test..."
echo "./crypto-api --password-hash test@123"
cd client/src && ./crypto-api --password-hash test@123 &
EXEC_STATUS
echo $DASHLINE
cd $CWD

#----Thoughts---
# later: deploy server and client separately if needed.
    # check environment
# Advanced: containerise. or am I ovethinking?!
#---------------