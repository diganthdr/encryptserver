#!/bin/bash    

# kill server
echo "Killing server.."
ps auxww | grep 'server.py' | awk '{print $2}' | xargs kill -9

# kill redis
echo "Killing redis.."
ps auxww | grep 'redis-server' | awk '{print $2}' | xargs kill -9

# kill all celery workers
echo "Killing celery workers"
ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill -9

echo "Shutdown server DONE!"
# TODO, Do a graceful shutdown, such as deamonise in services and start/stop service

