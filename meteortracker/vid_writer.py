from collections import deque
from datetime import datetime

import cv2


class VidWriter(object):
    def __init__(self, output_file=None, n_frames=120):
        output_dir = os.path.abspath(os.path.curdir)

        if output_file is None:
            output_file = datetime.now().isoformat() + ".avi"
        else:
            output_file += ".avi"

        self.output = os.path.join(output_dir, output_file)

        print("output file: ", self.output_file)

        self.n_frames = n_frames
        self.current_frame = 0

        four_cc = cv2.cv.FOURCC('I', 'Y', 'U', 'V')
        self.writer = cv2.VideoWriter(self.output, four_cc, 2, (1280, 720))

        if not self.writer.isOpened():
            raise IOError("Unable to open video stream")

        self.frames = deque([], maxlen=self.n_frames)

    def add_frame(self, frame):
        self.frames.append(frame)

    def write_frames_to_video(self):
        for frame in self.frames:
            self.writer.write(frame)

    def __del__(self):
        self.writer.release()
