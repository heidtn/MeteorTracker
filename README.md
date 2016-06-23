# MeteorTracker
Finds a user's position and triangulates meteor trajectories based on camera inputs.

# Project Elements
- Camera Calibration
- Setup process
- Orientation and location handling
- Anomaly detection and separation
- Meteor pairing (Server side)
- Iterative Linear Triangulation (Server Side)
- Server web page
- RPi web page


Here is the current layout of the file structure:
- camera.py - this generates an instance of video.  It can be a webcam, or if given a source, a video file (for testing)
- find_events.py - this compares two images and detects potential meteors.  It is a simple motion detector, that filters motion blobs by they're size and elongation.  It works in a basic sense, but will need more test data to refine
- MeteorTracker.py - this runs the show.  It instantiates a camera and collects images looking for meteor events.  
- server.py - a poor attempt at getting a live interactive server to work with the MeteorTracker.py code.  It needs to be redone at some point.
- vid_writer.py - intended for debugging purposes, this takes a number of frames and outputs a .avi file.

- parse_stars.py - this is a work in progress.  The idea is that the camera can find its orientation (and in the future, perhaps approximate location), based on its current view of the stars.


#Time line
- Compile anomalies in a folder and use a simple web server to show them
	- To do this we will start with a basic subtractive filter that detects sizable anomalies between frames
- We will then write algos to determine which anomalies are meteors (vs airplanes or satellites)
- We will then add camera calibration
	- This comes with the ability to setup camera calibration via server paired with config file
- We will then pair this with Astronometry.net or similar to determine current location 
- We will then pair several devices together to attempt to determine trajectories of meteors
	- This is the primary release point to try and gather public use data
- We will then set up a public server to host and analyze data as it comes in
- Refinement and next steps