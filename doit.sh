#!/bin/bash

# Loop through ports 1 to 65535
for port in {1..65535}; do
    # Use curl to attempt a connection to localhost on the current port
    curl -s -o /dev/null -m 1 -I http://127.0.0.1:$port >/dev/null 2>&1

    # Check the exit status of curl
    if [ $? -eq 0 ]; then
        echo "Port $port is open"
    fi
done

