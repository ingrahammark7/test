from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='static')

# Serve the HTML page at the root
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'terrain.html')

# Serve any file from the static folder, including subfolders
@app.route('/<path:filename>')
def serve_files(filename):
    file_path = os.path.join(app.static_folder, filename)
    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, filename)
    else:
        return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)