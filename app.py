from flask import Flask, render_template, Response,url_for, redirect, request
from camera import VideoCamera
import cv2
import time

app = Flask(__name__)

@app.route("/")
def home():
    # rendering web page
    return render_template('index.html')

def gen(camera):
    while True:
        # get camera frame
        frame = camera.photo_capture()
        yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen1(camera):
    while True:
        # get camera frame
        frame = camera.face_eyes_detect()
        yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen2(camera):
    while True:
        # get camera frame
        frame = camera.filters_apply()
        yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen3(camera):
    while True:
        # get camera frame
        frame = camera.photo_sketch()
        yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen4(camera):
    while True:
        # get camera frame
        frame = camera.qrcode_scanner()
        yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route("/video_feed")
def video_feed():
    return Response(gen(VideoCamera()),
          mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/video_feed1")
def video_feed1():
    return Response(gen1(VideoCamera()),
          mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/video_feed2")
def video_feed2():
    return Response(gen2(VideoCamera()),
          mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/video_feed3")
def video_feed3():
    return Response(gen3(VideoCamera()),
          mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/video_feed4")
def video_feed4():
    return Response(gen4(VideoCamera()),
          mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # defining server ip address and port
    app.run(debug=True)
