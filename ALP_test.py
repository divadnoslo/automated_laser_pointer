import cv2
import sys
from LP import LP
import numpy as np
import time
import face_detect as fd

#-------------------------------------------------------------------------------------------------------
# Initialize Camera
s = 0
if len(sys.argv) > 1:
    s = sys.argv[1]

source = cv2.VideoCapture(s)

win_name = 'Raspberry Pi Camera'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(win_name, 640, 480)

net = cv2.dnn.readNetFromCaffe("deploy.prototxt", \
                               "res10_300x300_ssd_iter_140000_fp16.caffemodel")

#-------------------------------------------------------------------------------------------------------
# Initialize LP (Laser Pointer)    

# Construct a LP object
lp = LP(delay = 0.05)

# Center the LP
lp.centerLP()

#-------------------------------------------------------------------------------------------------------
# Main Loop

# Begin Main Loop
while cv2.waitKey(1) != 27: # Press ESC Key to Exit Loop!
    
    # Capture Frame
    has_frame, frame = source.read()
    if not has_frame:
        break
    
    # Flip Frame for Webcam View
    frame = cv2.flip(frame,1)
    
    # Perform Face Detection
    frame, DETECT_FLAG, u_face, v_face = fd.faceDetect(net, frame)
    
    # If Face Detected
    if (DETECT_FLAG):
        
        # Only Adjust Azimuth for Now
        az_adj, el_adj = fd.centerFace(frame, u_face, v_face)
    
        # Move LP according to Adjustments
        lp.moveLP(az_adj, 0) # no el adjustment for now
    
    # Show Resulting Image
    cv2.imshow(win_name, frame)
    
#------------------------------------------------------------------------------------------------------
# Release Camera and Destory Window
source.release()
cv2.destroyWindow(win_name)

# Note: If this section of code does not run, you will need to run it in the cmd prompt
