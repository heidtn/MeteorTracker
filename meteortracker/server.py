"""
This is currently garbage and doesn't work
(Based on the gist by Igor Maculan - n3wtron@gmail.com).

Serves most current image for debug and general view.

"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import io
import time

from PIL import Image

from . import meteor_tracker


class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("access!")
        if self.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header('Content-type',
                             'multipart/x-mixed-replace; '
                             'boundary=--jpgboundary')
            self.end_headers()
            while True:
                try:
                    img = global_dict['lastest_image']
                    if img is None:
                        continue

                    jpg = Image.fromarray(img)
                    temp_file = io.StringIO()
                    jpg.save(temp_file, 'JPEG')
                    self.wfile.write("--jpgboundary")
                    self.send_header('Content-type', 'image/jpeg')
                    self.send_header('Content-length', str(temp_file.len))
                    self.end_headers()
                    jpg.save(self.wfile, 'JPEG')
                    time.sleep(0.05)
                except KeyboardInterrupt:
                    break
            return

        if self.path.endswith('.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('<html><head></head><body>')
            self.wfile.write('<img src="http://127.0.0.1:8080/cam.mjpg"/>')
            self.wfile.write('</body></html>')
            return


def main():
    global_dict = {'latest_image': None}
    tracker = meteor_tracker.Tracker(global_dict)
    tracker.set_daemon(True)
    tracker.start()

    server = HTTPServer(('', 8080), CamHandler)
    print("server started")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()


if __name__ == '__main__':
    main()
