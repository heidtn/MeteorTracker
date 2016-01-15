import cv2
from PIL import Image
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import StringIO
import time
import MeteorTracker

"""
(Based on the gist by Igor Maculan - n3wtron@gmail.com).  Serves most current image for debug and general view.
"""

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		print "access!"
		if self.path.endswith('.mjpg'):
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			while True:
				try:
					img = glbl_dict['lastestimage']
					if img is None:
						continue

					jpg = Image.fromarray(img)
					tmpFile = StringIO.StringIO()
					jpg.save(tmpFile,'JPEG')
					self.wfile.write("--jpgboundary")
					self.send_header('Content-type','image/jpeg')
					self.send_header('Content-length',str(tmpFile.len))
					self.end_headers()
					jpg.save(self.wfile,'JPEG')
					time.sleep(0.05)
				except KeyboardInterrupt:
					break
			return
		if self.path.endswith('.html'):
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<img src="http://127.0.0.1:8080/cam.mjpg"/>')
			self.wfile.write('</body></html>')
			return

def main():
	global glbl_dict
	glbl_dict = dict()
	glbl_dict['lastestimage'] = None
	t = MeteorTracker.Tracker(glbl_dict)
	t.setDaemon(True)
	t.start()


	try:
		server = HTTPServer(('',8080),CamHandler)
		print "server started"
		server.serve_forever()
	except KeyboardInterrupt:
		server.socket.close()

if __name__ == '__main__':
	main()
