from flask import Flask, render_template, Response
import cv2
import mediapipe as mp

app = Flask(__name__)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

drawingColors = [
    (51, 153, 255),  # Light blue
    (255, 0, 255),   # Pink
    (0, 255, 0),     # Green
    (255, 255, 0),   # Cyan
    (255, 0, 0)      # Blue
]
currentColorIndex = [0]
myPoints = []

def fingers_up(landmarks):
    return (landmarks[8][1] < landmarks[6][1] and
            landmarks[12][1] < landmarks[10][1] and
            landmarks[16][1] < landmarks[14][1] and
            landmarks[20][1] < landmarks[18][1])

def index_and_middle_up(landmarks):
    return (landmarks[8][1] < landmarks[6][1] and
            landmarks[12][1] < landmarks[10][1])

def erase_points(points, x_min, x_max, y_min, y_max):
    return [point for point in points if not (x_min < point[0] < x_max and y_min < point[1] < y_max)]

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    cap = cv2.VideoCapture(0)
    
    while True:
        success, frame = cap.read()
        if not success:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                landmarks = [(int(point.x * frame.shape[1]), int(point.y * frame.shape[0])) for point in hand_landmarks.landmark]

                if fingers_up(landmarks):
                    x_min, x_max = min([p[0] for p in landmarks]), max([p[0] for p in landmarks])
                    y_min, y_max = min([p[1] for p in landmarks]), max([p[1] for p in landmarks])
                    myPoints[:] = erase_points(myPoints, x_min, x_max, y_min, y_max)
                elif index_and_middle_up(landmarks):
                    currentColorIndex[0] = (currentColorIndex[0] + 1) % len(drawingColors)
                else:
                    x, y = landmarks[8]
                    myPoints.append((x, y, currentColorIndex[0]))

        for point in myPoints:
            cv2.circle(frame, (point[0], point[1]), 10, drawingColors[point[2]], cv2.FILLED)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
