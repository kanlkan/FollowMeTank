#gst-launch-1.0 nvarguscamerasrc ! nvoverlaysink
#gst-launch-1.0 nvarguscamerasrc sensor_mode=2 ! nvvidconv ! video/x-raw, format=BGRx ! videoconvert ! nvoverlaysink
gst-launch-1.0 nvarguscamerasrc sensor_mode=2 ! nvvidconv ! video/x-raw, format=I420 ! videoconvert ! nvoverlaysink
