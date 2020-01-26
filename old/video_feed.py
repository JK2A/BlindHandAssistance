import cv2
import numpy as np
import time


import handtracking.utils.detector_utils as du
#from handtracking.utils.detector_utils import load_inference_graph
#from handtracking.utils.detector_utils import detect_objects

cap = cv2.VideoCapture(0)

graph = du.load_inference_graph()

#graph = load_inference_graph()

while(True):
    ret, frame = cap.read()

    # Our operations on the frame come here
    # Display the resulting frame
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
