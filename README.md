# py-stopmotion
Uses opencv-python and imageio to implement barebones stop-motion capture, with onion-skinning, from any webcam that OpenCV can see.

Now, also works with DSLRs using python-gphoto2!

Works for Mac.

Call from the command line:
```bash
$ python stopmotion.py [captureDevice] [direc] [savegif]
```

* captureDevice: the id of the webcam for OpenCV (try 0, 1, 2,...) OR -1 for a DSLR connected via USB
* direc: the directory to save frames to
* savegif: a boolean for whether to save a gif in the same directory

capture frames with Return, quit and save with Esc.

The end
