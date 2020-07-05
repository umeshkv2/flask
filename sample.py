import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)
        
    cv2.imshow('Image', frame)
    count_faces = str(len(faces))
   
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
    
print('number of faces : ', count_faces)
cap.release()
cv2.destroyAllWindows()

