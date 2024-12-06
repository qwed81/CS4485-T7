#!/bin/sh

# Start the first process
 python ./jupyter.py &

# Start the second process
 jupyter notebook --no-browser --allow-root &

# Wait for any process to exit
 wait -n

# Exit with status of process that exited first
 exit $?

