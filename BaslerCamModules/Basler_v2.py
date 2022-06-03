import pypylon.pylon as py
import numpy as np
import os
import cv2
import time

last_timestamp = 0
timestamp = 0

# Simply get the first available pylon device.
first_device = py.TlFactory.GetInstance().CreateFirstDevice()
instant_camera = py.InstantCamera(first_device)
instant_camera.Open()

# Optional if you set it in Pylon Viewer
instant_camera.PixelFormat = "BayerRG8"

instant_camera.StartGrabbing(py.GrabStrategy_LatestImages)


size = (1920, 1200)


while True:
    # Update current image in video window.
    # Grab one image.
    #global resul
    c = 0
    img = np.zeros((1, 1))
    if instant_camera.NumReadyBuffers:
        res = instant_camera.RetrieveResult(1000)
        if res:
            try:
                if res.GrabSucceeded():
                    currImg = res.Array
                    currImg = cv2.cvtColor(currImg, cv2.COLOR_BayerRG2RGB)
           ######         if you want to save image, uncomment line 54 and 55

                    #text = "image.png"
                    #cv2.imwrite(text,currImg)
                    cv2.imshow("frr", currImg)

                    print("writing..")
                    #result.write(fr)
                    
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

        print("FPS:" ,frame_rate)
    # Wait    1 ms.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
