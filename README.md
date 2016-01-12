# MeteorTracker
Finds a user's position and triangulates meteor trajectories based on camera inputs.

#Time line
- Compile anomalies in a folder and use a simple web server to show them
	- To do this we will start with a basic subtractive filter that detects sizable anomalies between frames
- We will then write algos to determine which anomalies are meteors
- We will then add camera calibration
	- This comes with the ability to setup camera calibration via server paired with config file
- We will then pair this with Astronometry.net or similar to determine current location 
- We will then pair several devices together to attempt to determine trajectories of meteors
	- This is the primary release point to try and gather public use data
- We will then set up a public server to host and analyze data as it comes in
- Refinement and next steps