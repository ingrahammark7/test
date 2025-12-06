# debug_server.py
import http.server
import socketserver
import os
import signal
import sys

PORT = 8000
FILENAME = "f.json"

class DebugHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print(f"Request path: {self.path}")
        if self.path.endswith(FILENAME):
            try:
                filesize = os.path.getsize(FILENAME)
                print(f"Serving {FILENAME} ({filesize} bytes)")
                with open(FILENAME, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                print("Error reading file:", e)
                self.send_error(500, "Internal Server Error")
        else:
            # fallback to default behavior
            super().do_GET()

class GracefulTCPServer(socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True  # threads die when main thread exits

def shutdown_server(signum, frame):
    print("Shutting down server...")
    sys.exit(0)

if __name__ == "__main__":
    # handle Ctrl+C and termination signals
    signal.signal(signal.SIGINT, shutdown_server)
    signal.signal(signal.SIGTERM, shutdown_server)

    with GracefulTCPServer(("", PORT), DebugHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server stopped by user")