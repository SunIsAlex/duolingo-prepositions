#!/bin/bash
fuser -k 8080/tcp 2>/dev/null || pkill -f "server\.py" 2>/dev/null || true
echo "🛑 Server stopped."
