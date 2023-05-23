#!/bin/bash

# Find the PID of detect_faces.py
pid=$(pgrep -f detect_faces.py)

# Check if the pid exists
if [ ! -z "$pid" ]; then
    echo "detect_faces.py is currently running with PID: $pid"
else
    echo "No running process found for detect_faces.py"
fi
