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
import socket
from datetime import datetime, timezone
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = int(os.environ.get('PORT', 8080))
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public')
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
PROGRESS_FILE = os.path.join(DATA_DIR, 'progress.json')

# Import Zuoyebang Crawler integration
try:
    from zyb_importer import crawl_zuoyebang_link, ZYB_CURATED_QUESTIONS
except ImportError:
    crawl_zuoyebang_link = None
    ZYB_CURATED_QUESTIONS = []

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

        if self.path == '/api/zyb/crawl':
            try:
                length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(length)
                payload = json.loads(body.decode('utf-8')) if body else {}
                url = payload.get('url', '').strip()
                urls = payload.get('urls', [])
                if url and url not in urls:
                    urls.append(url)

                if not urls:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "error", "message": "请提供有效的作业帮分享链接"}).encode('utf-8'))
                    return

                new_questions = []
                errors = []
                for u in urls:
                    try:
                        qs = crawl_zuoyebang_link(u)
                        new_questions.extend(qs)
                    except Exception as err:
                        errors.append(f"{u}: {str(err)}")

                # Persist imported questions into progress.json
                prog = {}
                if os.path.exists(PROGRESS_FILE):
                    try:
                        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                            prog = json.load(f)
                    except Exception:
                        prog = {}

                custom = prog.get('customQuestions', [])
                existing_ids = set(q.get('id') for q in custom)
                added_count = 0
                for q in new_questions:
                    if q['id'] not in existing_ids:
                        custom.append(q)
                        existing_ids.add(q['id'])
                        added_count += 1

                prog['customQuestions'] = custom
                prog['updatedAt'] = datetime.now(timezone.utc).isoformat()

                temp_file = PROGRESS_FILE + '.tmp'
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(prog, f, ensure_ascii=False, indent=2)
                os.replace(temp_file, PROGRESS_FILE)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                resp = {
                    "status": "ok",
                    "importedCount": added_count,
                    "questions": new_questions,
                    "errors": errors,
                    "message": f"成功爬取并解析导入 {added_count} 道英语题目！"
                }
                self.wfile.write(json.dumps(resp, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "error": str(e)}).encode('utf-8'))
            return

        if self.path == '/api/zyb/preload':
            try:
                # Preload curated Zuoyebang exam questions
                prog = {}
                if os.path.exists(PROGRESS_FILE):
                    try:
                        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                            prog = json.load(f)
                    except Exception:
                        prog = {}

                custom = prog.get('customQuestions', [])
                existing_ids = set(q.get('id') for q in custom)
                added = 0
                for q in ZYB_CURATED_QUESTIONS:
                    if q['id'] not in existing_ids:
                        custom.append(q)
                        existing_ids.add(q['id'])
                        added += 1

                prog['customQuestions'] = custom
                prog['updatedAt'] = datetime.now(timezone.utc).isoformat()

                temp_file = PROGRESS_FILE + '.tmp'
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(prog, f, ensure_ascii=False, indent=2)
                os.replace(temp_file, PROGRESS_FILE)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "ok",
                    "addedCount": added,
                    "totalCurated": len(ZYB_CURATED_QUESTIONS),
                    "message": f"成功载入 {added} 道精选作业帮与高考真题！"
                }, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "error": str(e)}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

class DuolingoServer(HTTPServer):
    allow_reuse_address = True

def daemonize():
    """
    Auto-daemonize unless --foreground or NO_DAEMON=1 is specified.
    If already running on PORT, exit cleanly with 0.
    """
    if '--foreground' in sys.argv or os.environ.get('NO_DAEMON') == '1':
        return

    # Check if another instance is already listening on PORT
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(0.5)
        s.connect(('127.0.0.1', PORT))
        s.close()
        print(f"==================================================")
        print(f"🦉 Duolingo Prepositions Web App is already running on port {PORT}!")
        print(f"📱 Local URL:   http://localhost:{PORT}")
        print(f"🌐 Network URL: http://192.168.0.101:{PORT}")
        print(f"==================================================")
        sys.exit(0)
    except (OSError, socket.error):
        pass
    finally:
        try:
            s.close()
        except Exception:
            pass

    # First fork (detaches from parent)
    try:
        pid = os.fork()
        if pid > 0:
            print(f"==================================================")
            print(f"🦉 Duolingo Prepositions Web App is running in background!")
            print(f"📱 Local URL:   http://localhost:{PORT}")
            print(f"🌐 Network URL: http://192.168.0.101:{PORT}")
            print(f"💾 Storage API: http://localhost:{PORT}/api/progress")
            print(f"📂 Root Dir:    {BASE_DIR}")
            print(f"==================================================")
            sys.exit(0)
    except OSError as e:
        print(f"Fork #1 failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Decouple from parent environment
    os.setsid()
    os.umask(0)

    # Second fork (prevent acquiring controlling terminal)
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        print(f"Fork #2 failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Redirect standard file descriptors to server.log
    sys.stdout.flush()
    sys.stderr.flush()
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'server.log')
    try:
        si = open(os.devnull, 'r')
        so = open(log_file, 'a+', buffering=1)
        se = open(log_file, 'a+', buffering=1)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
    except Exception:
        pass

def main():
    daemonize()

    server_address = ('0.0.0.0', PORT)
    httpd = DuolingoServer(server_address, DuolingoHandler)
    if '--foreground' in sys.argv or os.environ.get('NO_DAEMON') == '1':
        print(f"==================================================")
        print(f"🦉 Duolingo Prepositions Web App is running (foreground)!")
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
