#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

# Check if already running
if pgrep -f "python3 server.py" > /dev/null; then
    echo "Server is already running on port 8080."
    echo "Visit: http://localhost:8080"
    exit 0
fi

setsid python3 server.py > server.log 2>&1 < /dev/null &
sleep 1

if pgrep -f "python3 server.py" > /dev/null; then
    echo "✅ Duolingo Prepositions App successfully started!"
    echo "📱 Local Browser:   http://localhost:8080"
    echo "🌐 LAN Devices:     http://192.168.0.101:8080"
else
    echo "❌ Failed to start server. Check server.log:"
    cat server.log
fi
