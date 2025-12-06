# debug_server.py
import http.server
import socketserver
import os

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

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), DebugHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()