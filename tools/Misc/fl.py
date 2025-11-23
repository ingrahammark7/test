from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='static')

# Serve the HTML page
@app.route('/')
def index():
    return send_from_directory('static', 'terrain.html')

# Serve JSON files automatically
@app.route('/<path:filename>')
def serve_files(filename):
    return send_from_directory('', filename)

if __name__ == '__main__':
    app.run(debug=True)