import json
import os
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs

root = Path(os.environ.get('DATA_DIR', '/data'))
root.mkdir(parents=True, exist_ok=True)
db = sqlite3.connect(root / 'notes.sqlite3')
db.execute('create table if not exists notes (body text not null)')

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'healthy')
            return
        if self.path == '/api/notes':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps([row[0] for row in db.execute('select body from notes')]).encode())
            return
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<title>Zenith image proof</title><h1>Notes</h1><form method="post"><label>Note <input name="body" required></label><button>Save</button></form>')

    def do_POST(self):
        size = int(self.headers.get('Content-Length', '0'))
        if size > 4096:
            self.send_error(413)
            return
        body = parse_qs(self.rfile.read(size).decode()).get('body', [''])[0]
        db.execute('insert into notes(body) values (?)', (body,))
        db.commit()
        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

HTTPServer(('0.0.0.0', int(os.environ.get('PORT', '8080'))), Handler).serve_forever()
