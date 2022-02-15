import pypylon.pylon as py
import numpy as np
import cv2
import time  
from New_ObjectDimension_v2 import *
#from New_ProductSorting_v2 import *

last_timestamp = 0
timestamp = 0

# Simply get the first available pylon device.
first_device = py.TlFactory.GetInstance().CreateFirstDevice()
instant_camera = py.InstantCamera(first_device)
instant_camera.Open()

# Optional if you set it in Pylon Viewer
instant_camera.PixelFormat = "BayerRG8"

instant_camera.StartGrabbing(py.GrabStrategy_LatestImages)


while True:
    # Update current image in video window.
    # Grab one image.
    img = np.zeros((1, 1))
    if instant_camera.NumReadyBuffers:
        res = instant_camera.RetrieveResult(1000)
        if res:
            try:
                if res.GrabSucceeded():
                    currImg = res.Array
                    currImg = cv2.cvtColor(currImg,cv2.COLOR_GRAY2RGB)
                    ObjDim(currImg)  # Object Dimension detection
                    #ProdSort(currImg)   # Product Sorting
                    
            finally:
                res.Release()

    timestamp = time.time()
    if 0 == last_timestamp:
        last_timestamp = timestamp
    else:
        period = timestamp - last_timestamp
        last_timestamp = timestamp

        frame_rate = 1 / period
        frametime = period

        print(frame_rate)
    # Wait    1 ms.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
