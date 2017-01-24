# MeteorTracker
This is a project that uses a Raspberry pi (or any computer), a webcam, some computer vision, and some math to triangulate the trajectories of meteors as they hit the atmosphere and light up.

The camera will capture events using pretty basic computer vision techniques. It will then upload this image to a server along with its geolocation and orientation (and other data such as camera parameters). The server will match simultaneous events and triangulate possible landing spaces as well as entry trajectories.

The primary goal is to find fallen meteors for scientific and hobbyist purposes and to help us understand more about our universe. Also by charting entries we can estimate the orbit of the meteoroid. Small meteoroids tend to serve as early warnings of larger ones as meteors tend to travel in similar orbits, so this could be an early warning system!


# Setup
You'll need a computer with python (2.7 as of now) and opencv.  You'll also need an openCV compatible camera.  Lower light cameras are better.  The camera should be oriented orthogonally to the ground (i.e. up).  Run setup.py first.  Then run MeteorTracker.py and you're good to go.

<div style="text-align:center"><img src ="MeteorCapture.png?raw=true" /></div>

# Project Elements
- Camera Calibration
- Setup process
- Orientation and location handling
- Anomaly detection and separation
- Meteor pairing (Server side)
- Iterative Linear Triangulation (Server Side)
- Server web page
- RPi web page

# layout
Here is the current layout of the file structure:
- Camera.py - this generates an instance of video.  It can be a webcam, or if given a source, a video file (for testing)
- FindEvents.py - this compares two images and detects potential meteors.  It is a simple motion detector, that filters motion blobs by they're size and elongation.  It works in a basic sense, but will need more test data to refine
- MeteorTracker.py - this runs the show.  It instantiates a camera and collects images looking for meteor events.  
- VideWrited.py - intended for debugging purposes, this takes a number of frames and outputs a .avi file.

TODO:
- ParseStars.py - this is a work in progress.  The idea is that the camera can find its orientation (and in the future, perhaps approximate location), based on its current view of the stars and the current time.
- server.py - a poor attempt at getting a live interactive server to work with the MeteorTracker.py code.  It needs to be redone at some point.
- skew line measurement between events from separate cameras
- multiple image sequence line drawing and correlation for triangulation
- we pass events around as dictionaries, create a class that encapsulates this information