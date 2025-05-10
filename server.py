from flask import Flask, Response
from color_detection import color_detection_stream

app = Flask(__name__)

@app.route('/stream')
def stream():
    return Response(color_detection_stream(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
