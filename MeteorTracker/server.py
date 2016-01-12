#!/usr/bin/env python
from flask import Flask, render_template, Response
import cv2
import os
import threading
import Queue
import camera

app = Flask(__name__)

queue = Queue.Queue()

@app.route('/')
def index():
	eventpics = os.listdir('static/eventpics/')
	return render_template('index.html', eventpics=eventpics)

def gen(camera):
	print "here"
	while True:
		frame = camera.getFrame()
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tostring() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(camera.camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
def main():
	app.run(host='0.0.0.0', debug=True)

if __name__=="__main__":
	main()