import cv2
import numpy as np
import mediapipe as mp

# Set the frame width and height
frameWidth = 640
frameHeight = 480

# Initialize webcam capture
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# Define possible drawing colors in BGR
drawingColors = [
    [51, 153, 255],  # Light blue
    [255, 0, 255],   # Pink
    [0, 255, 0],     # Green
    [255, 255, 0],   # Cyan
    [255, 0, 0]      # Blue
]
currentColorIndex = 0
drawingColor = drawingColors[currentColorIndex]

# Initialize list to store drawing points
myPoints = []  # [x, y, colorId]

# Function to draw on the canvas
def AirDraw(myPoints, drawingColors):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, drawingColors[point[2]], cv2.FILLED)

# Function to check if all fingers are up
def fingersUp(hand_landmarks):
    finger_tips_ids = [mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.INDEX_FINGER_TIP, 
                       mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP, 
                       mp_hands.HandLandmark.PINKY_TIP]
    for i in finger_tips_ids:
        if hand_landmarks.landmark[i].y > hand_landmarks.landmark[i - 2].y:
            return False
    return True

# Function to check if index and middle fingers are up
def indexAndMiddleUp(hand_landmarks):
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
    index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
    middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
    
    return index_tip < index_pip and middle_tip < middle_pip

# Function to delete points within the hand area
def erasePoints(myPoints, hand_landmarks, h, w):
    x_min = min([lm.x for lm in hand_landmarks.landmark]) * w
    x_max = max([lm.x for lm in hand_landmarks.landmark]) * w
    y_min = min([lm.y for lm in hand_landmarks.landmark]) * h
    y_max = max([lm.y for lm in hand_landmarks.landmark]) * h
    
    new_points = []
    for point in myPoints:
        if not (x_min < point[0] < x_max and y_min < point[1] < y_max):
            new_points.append(point)
    return new_points

# Main loop
while True:
    success, img = cap.read()
    if not success:
        break

    imgResult = img.copy()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(imgResult, handLms, mp_hands.HAND_CONNECTIONS)
            index_finger_tip = handLms.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            h, w, c = imgResult.shape
            cx, cy = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
            
            if fingersUp(handLms):
                myPoints = erasePoints(myPoints, handLms, h, w)
            elif indexAndMiddleUp(handLms):
                currentColorIndex = (currentColorIndex + 1) % len(drawingColors)
                drawingColor = drawingColors[currentColorIndex]
            else:
                myPoints.append([cx, cy, currentColorIndex])

    if len(myPoints) != 0:
        AirDraw(myPoints, drawingColors)

    cv2.imshow("Result", imgResult)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
