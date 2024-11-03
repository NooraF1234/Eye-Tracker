from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('', 'index.html')

@app.route('/Eye_tracking_data/<path:filename>')
def send_eye_tracking_data(filename):
    return send_from_directory('Eye_tracking_data', filename)

if __name__ == '__main__':
    app.run(debug=True)

