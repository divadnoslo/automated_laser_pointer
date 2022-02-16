import cv2
import numpy as np

# Build Face Detection Function to Clean Up Code
def faceDetect(net, frame):
    
    # DNN Model parameters
    in_width = 300
    in_height = 300
    mean = [104, 117, 123]
    conf_threshold = 0.7
    
    # Frame Parameters
    frame_height = frame.shape[0]
    frame_width = frame.shape[1]

    # Create a 4D blob from a frame.
    blob = cv2.dnn.blobFromImage(frame, 1.0, (in_width, in_height), mean, swapRB = False, crop = False)
    
    # Run the Face Detection Model provided by OpenCV
    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x_left_bottom = int(detections[0, 0, i, 3] * frame_width)
            y_left_bottom = int(detections[0, 0, i, 4] * frame_height)
            x_right_top = int(detections[0, 0, i, 5] * frame_width)
            y_right_top = int(detections[0, 0, i, 6] * frame_height)

            cv2.rectangle(frame, (x_left_bottom, y_left_bottom), (x_right_top, y_right_top), (0, 255, 0))
            label = "Confidence: %.4f" % confidence
            label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

            cv2.rectangle(frame, (x_left_bottom, y_left_bottom - label_size[1]),
                                (x_left_bottom + label_size[0], y_left_bottom + base_line),
                                (255, 255, 255), cv2.FILLED)
            cv2.putText(frame, label, (x_left_bottom, y_left_bottom),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

            # t, _ = net.getPerfProfile()
            # label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
            center = [(x_right_top - x_left_bottom)/2 + x_left_bottom, \
                      (y_right_top - y_left_bottom)/2 + y_left_bottom]
            center[0] = int(center[0])   
            center[1] = int(center[1]) 
            cv2.circle(frame, (center[0], center[1]), 10, (255, 0, 255), 2)  
            label1 = 'Face Center at: %s px across, ' % center[0]
            label2 = '%s px down' % center[1]
            label = label1 + label2
            cv2.putText(frame, label, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
            DETECT_FLAG = True
            
        else:
            center = [int(frame.shape[0]/2), int(frame.shape[1]/2)]
            DETECT_FLAG = False
    
    # Return new frame and face detection coordinates
    u_face = center[0]
    v_face = center[1]
    return frame, DETECT_FLAG, u_face, v_face
    
#-------------------------------------------------------------------------------------------------------------
# Low-Grade "Control" System

def centerFace(frame, u_face, v_face):
    
    # Frame Parameters
    frame_height = frame.shape[0]
    frame_width = frame.shape[1]
    u_center = frame_height / 2
    v_center = frame_width / 2
    
    # Determine Error From Center
    du = u_face - u_center
    dv = v_face - v_center
    
    # Determine Az Adjustment (1 degree adjustments for now)
    if (np.abs(dv) <= 20):
        az_adj = 0
    elif (dv > 0):
        az_adj = -1
    elif (dv < 0):
        az_adj = 1
    else:
        az_adj = 0
        
    # Determine El Adjustment (1 degree adjustments for now)
    if (np.abs(du) <= 20):
        el_adj = 0
    elif (du > 0):
        el_adj = -1
    elif (du < 0):
        el_adj = 1
    else:
        el_adj = 0
        
        
    # Return Function Outputs
    return az_adj, el_adj
    
    