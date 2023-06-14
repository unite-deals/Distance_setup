from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

camera = cv2.VideoCapture(0)
points = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return jsonify({'result': get_frame().tolist()})

def get_frame():
    _, frame = camera.read()
    frame = cv2.flip(frame, 1)
    return frame

@app.route('/capture_point', methods=['POST'])
def capture_point():
    point = request.get_json()
    points.append(point)
    return jsonify({'result': 'success'})

@app.route('/calculate_distance', methods=['POST'])
def calculate_distance():
    distance = 0
    for i in range(len(points) - 1):
        point1 = np.array(points[i])
        point2 = np.array(points[i + 1])
        dist = np.linalg.norm(point2 - point1)
        distance += dist
    return jsonify({'result': distance})

if __name__ == '__main__':
    app.run()

camera.release()
cv2.destroyAllWindows()
