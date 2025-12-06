# dynamic_server.py
import http.server
import socketserver
import os
import signal
import sys
from urllib.parse import urlparse

PORT = 8000
JSON_FILES = ["f.json", "f2.json", "f3.json"]

class DynamicHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.lstrip('/')
        print(f"Request path: {path}")
        
        if path in JSON_FILES:
            try:
                filesize = os.path.getsize(path)
                print(f"Serving {path} ({filesize} bytes)")
                with open(path, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Content-Length", str(len(content)))
                # disable caching completely
                self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
                self.send_header("Pragma", "no-cache")
                self.send_header("Expires", "0")
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                print("Error reading file:", e)
                self.send_error(500, "Internal Server Error")
        else:
            # fallback to default handler for HTML/JS
            super().do_GET()

class GracefulTCPServer(socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

def shutdown_server(signum, frame):
    print("Shutting down server...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown_server)
    signal.signal(signal.SIGTERM, shutdown_server)

    with GracefulTCPServer(("", PORT), DynamicHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server stopped by user")