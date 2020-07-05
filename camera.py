import cv2
import numpy as np
import scipy.ndimage
import pyzbar.pyzbar as pyzbar
from PIL import Image

# defining face detector
face_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')

class VideoCamera(object):
    def __init__(self):
        # capturing video
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        # releasing camera
        self.video.release()

    def photo_capture(self):
        ret, frame = self.video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        c = 0
        while True:
            k = cv2.waitKey(1000) & 0xFF
            print("Image "+str(c)+" saved")
            file = 'C:/Users/user/Desktop/flask/images/'+str(c)+'.jpg'
            cv2.imwrite(file, frame)
            c += 1
        '''count_faces = str(len(faces))

        print('number of faces: ', count_faces)'''        
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
    
                
    def face_eyes_detect(self):
        ret, frame = self.video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

        
        # encode Opencv raw frame to jpg and display it
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def filters_apply(self):
        ret, frame = self.video.read()
        edges = cv2.Canny(frame, 100, 200)
        # encode Opencv raw frame to jpg and display it
        ret, jpeg = cv2.imencode('.jpg', edges)
        return jpeg.tobytes()

    def photo_sketch(self):
        ret, frame = self.video.read()

        def grayscale(rgb):
            return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])
        gray = grayscale(frame)
        
        inverse = 255 - gray

        blur = scipy.ndimage.filters.gaussian_filter(inverse, sigma=20)

        def dodge(front, back):
            result=front*255/(255-back)
            result[result>255]=255
            result[back==255]=255
            return result.astype('uint8')
        final = dodge(blur, gray)
        _, jpeg = cv2.imencode('.jpg', final)
        return jpeg.tobytes()

    def qrcode_scanner(self):
        ret, frame = self.video.read()
        font = cv2.FONT_HERSHEY_SIMPLEX
        qrcode = pyzbar.decode(frame)

        for obj in qrcode:
            print('Data \n', obj.data)
            #cv2.putText(frame, str(obj.data), (10, 10), font, 3, (255, 0, 0), 3)            

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
