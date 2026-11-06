#!/bin/bash
PID=$(pgrep -f "python3 server.py")
if [ -n "$PID" ]; then
    kill -9 $PID
    echo "🛑 Server (PID $PID) stopped."
else
    echo "Server is not running."
fi
