#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Duolingo Prepositions Web Application Server
Serves static files from public/ with proper MIME types and headers.
Provides API endpoints to persist and synchronize study progress to data/progress.json.
"""

import os
import sys
import json
import mimetypes
from datetime import datetime, timezone
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = int(os.environ.get('PORT', 8080))
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public')
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
PROGRESS_FILE = os.path.join(DATA_DIR, 'progress.json')

os.makedirs(DATA_DIR, exist_ok=True)

# Ensure correct MIME types
mimetypes.init()
mimetypes.add_type('application/json', '.json')
mimetypes.add_type('text/javascript', '.js')
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('audio/mpeg', '.mp3')
mimetypes.add_type('image/svg+xml', '.svg')

DEFAULT_PROGRESS = {
    "streak": 1,
    "lastActiveDate": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    "xp": 0,
    "totalAnswered": 0,
    "totalCorrect": 0,
    "history": {},
    "mistakes": [],
    "customQuestions": [],
    "updatedAt": datetime.now(timezone.utc).isoformat()
}

class DuolingoHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        # Enable CORS and disable overly aggressive caching during development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_HEAD(self):
        if self.path == '/api/progress':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            return
        super().do_HEAD()

    def do_GET(self):
        if self.path == '/api/progress':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()

            if os.path.exists(PROGRESS_FILE):
                try:
                    with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
                    return
                except Exception as e:
                    print(f"Error reading progress file: {e}")

            # Fallback to default progress
            self.wfile.write(json.dumps(DEFAULT_PROGRESS, ensure_ascii=False).encode('utf-8'))
            return

        super().do_GET()

    def do_POST(self):
        if self.path == '/api/progress':
            try:
                length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(length)
                data = json.loads(body.decode('utf-8'))

                data['updatedAt'] = datetime.now(timezone.utc).isoformat()

                # Atomic write
                temp_file = PROGRESS_FILE + '.tmp'
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                os.replace(temp_file, PROGRESS_FILE)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                resp = {"status": "ok", "message": "Progress stored successfully", "updatedAt": data['updatedAt']}
                self.wfile.write(json.dumps(resp).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "error": str(e)}).encode('utf-8'))
            return

        if self.path == '/api/progress/reset':
            try:
                if os.path.exists(PROGRESS_FILE):
                    os.remove(PROGRESS_FILE)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "message": "Progress reset successfully"}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "error": str(e)}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

def main():
    server_address = ('0.0.0.0', PORT)
    httpd = HTTPServer(server_address, DuolingoHandler)
    print(f"==================================================")
    print(f"🦉 Duolingo Prepositions Web App is running!")
    print(f"📱 Local URL:   http://localhost:{PORT}")
    print(f"🌐 Network URL: http://192.168.0.101:{PORT}")
    print(f"💾 Storage API: http://localhost:{PORT}/api/progress")
    print(f"📂 Root Dir:    {BASE_DIR}")
    print(f"==================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()

if __name__ == '__main__':
    main()
