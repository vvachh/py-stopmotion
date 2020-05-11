# py-stopmotion
Uses opencv-python and imageio to implement barebones stop-motion capture, with onion-skinning, from any webcam that OpenCV can see.

Call from the command line:
```bash
$ python stopmotion.py [captureDevice] [direc] [savegif]
```

* captureDevice: the id of the webcam for OpenCV (try 0, 1, 2,...)
* direc: the directory to save frames to
* savegif: a boolean for whether to save a gif in the same directory

capture frames with Return, quit and save with Esc.

The end