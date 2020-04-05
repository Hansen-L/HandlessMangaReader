import cv2
import sys
import logging as log
from time import sleep
from acs import send
import os
import datetime as dt
from pynput.keyboard import Key, Controller
import time


def detect_direction(pitch, yaw):
    if yaw > 8:
        return 'left'
    if yaw < -8:
        return 'right'
    if pitch > 15 :
        return 'up'
    if pitch < -5:
        return 'down'

    return None


cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='webcam.log',level=log.INFO)

video_capture = cv2.VideoCapture(0)
anterior = 0

keyboard = Controller()  # Initializing controller

font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (50, 50)
fontScale = 1
fontColor = (255, 255, 255)
lineType = 2

direction = None

prevtime = dt.datetime.now()

while True:  # Infinite loop to get video, create bounding box,
    if not video_capture.isOpened():  # If webcam is not working
        print('Unable to load camera.')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()  # Take frame from webcam
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # converts to grayscale
    faces = faceCascade.detectMultiScale(  # Detects faces, stores the coordinates of the faces for boxes
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )


    # Display the resulting frame
    if direction:
        cv2.putText(frame, direction,
                    bottomLeftCornerOfText,
                    font,
                    fontScale,
                    fontColor,
                    lineType)

    cv2.imshow('Video', frame)


    curtime = dt.datetime.now()

    wait_time = 0.5 # time between api queries
    if direction:
        wait_time = 2

    # API call only runs once every five seconds at most
    if abs((prevtime - curtime).total_seconds()) > wait_time:
        prevtime = curtime

        try:
            cv2.imwrite("image.jpg", frame)

            # Send jpg to azure cognitive services and get the faceattributes
            image_directory = os.path.dirname(__file__) + '/image.jpg'
            response = send(image_directory)
            print(response)

            if response:  # If a face is detected, get the pitch and yaw of the face
                face_attributes = response[0]['faceAttributes']
                headPose = face_attributes['headPose']
                pitch = headPose['pitch']
                yaw = headPose['yaw']

                direction = detect_direction(pitch, yaw)  # Call a function to return up, right, left or down or None
                print(direction)

                if direction: # If we detect a direction, do the corresponding key using keyboard controller
                    if direction == 'left':
                        keyboard.press(Key.left)
                        keyboard.release(Key.left)
                    elif direction == 'right':
                        keyboard.press(Key.right)
                        keyboard.release(Key.right)
                    elif direction == 'up':
                        for i in range(0,10):
                            keyboard.press(Key.up)
                            keyboard.release(Key.up)
                    elif direction == 'down':
                        for i in range(0, 10):
                            keyboard.press(Key.down)
                            keyboard.release(Key.down)

        except:
            print("API limit exhausted")


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
