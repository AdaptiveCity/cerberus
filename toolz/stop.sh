#!/bin/bash

# Find the PID of detect_faces.py
pid=$(pgrep -f detect_faces.py)

# Check if the pid exists
if [ ! -z "$pid" ]; then
    echo "Killing detect_faces.py with PID: $pid"
    
    # Kill the process
    kill -9 $pid

    echo "Process killed."
else
    echo "No running process found for detect_faces.py"
fi
